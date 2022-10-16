from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, Recipe, IngredientRecipe,
                            ShoppingCart, Tag)
from users.models import Follow, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerialiser,
                          ShoppingCartSerializer, ShowSubscriptionsSerializer,
                          SubscriptionSerializer, TagSerializer)


class SubscribeView(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Subscribe & unsubscribe."""

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Follow.objects.all()

    def create(self, serializer, **kwargs):
        author = get_object_or_404(
            User,
            pk=self.kwargs.get('author_id'),
        )
        Follow.objects.create(author=author, user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, serializer, *args, **kwargs):
        author = get_object_or_404(
            User,
            pk=self.kwargs.get('author_id'),
        )
        Follow.objects.filter(author=author, user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShowSubscriptionsView(viewsets.ReadOnlyModelViewSet):
    """Show subscriptions."""

    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = ShowSubscriptionsSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class FavoriteView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Add & delete recipes."""

    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        recipe = get_object_or_404(Favorite, user=self.request.user)
        return recipe

    def create(self, serializer, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id')
        )
        Favorite.objects.create(recipe=recipe, user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, serializer, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id')
        )
        Favorite.objects.filter(recipe=recipe, user=self.request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """List tags."""

    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """List ingredients."""

    permission_classes = [AllowAny, ]
    pagination_class = None
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Add & update & delete & list recipes."""

    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = CustomPagination
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return RecipeSerialiser
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class ShoppingCartView(mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """Add & delete & download shopping cart."""

    permission_classes = [IsAuthenticated, ]
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()

    def get_queryset(self):
        recipe = get_object_or_404(ShoppingCart, user=self.request.user)
        return recipe

    def create(self, serializer, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id')
        )
        ShoppingCart.objects.create(recipe=recipe, user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, serializer, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe,
            pk=self.kwargs.get('recipe_id')
        )
        ShoppingCart.objects.filter(
            recipe=recipe, user=self.request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def download_list(self, serializer, **kwargs):
        ingredient_list = "Cписок покупок:"
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=self.request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        for num, i in enumerate(ingredients):
            ingredient_list += (
                f"\n{i['ingredient__name']} - "
                f"{i['amount']} {i['ingredient__measurement_unit']}"
            )
            if num < ingredients.count() - 1:
                ingredient_list += ', '
        file = 'shopping_list'
        response = HttpResponse(
            ingredient_list, 'Content-Type: application/pdf'
        )
        response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response
