from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Follow

from recipes.models import (Favorite, Ingredient, Recipe, IngredientRecipe,
                            ShoppingCart, Tag)
from users.models import Follow, User

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from api.serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerialiser,
                          ShoppingCartSerializer, ShowSubscriptionsSerializer,
                          SubscriptionSerializer, TagSerializer)


class SubscribeView(viewsets.ModelViewSet):
    """Subscribe & unsubscribe. """

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        author = get_object_or_404(
            User,
            pk=self.kwargs.get('author_id'),
        )
        serializer.save(author=author, user=self.request.user)

    def get_queryset(self):
        author = get_object_or_404(
            Follow,
            authoer=self.kwargs.get('author_id')
        )
        return author.follower.all()

class ShowSubscriptionsView(viewsets.ReadOnlyModelViewSet):
    """Show subscriptions."""

    #permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = ShowSubscriptionsSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)

class FavoriteView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Add & delete favorite recipes."""

    # takes 1 positional argument but 2 were given
    #permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """List tags."""

    permission_classes = [AllowAny, ]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """List ingredients."""

    permission_classes = [AllowAny, ]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    """Add & update & delete & list recipes."""

    #permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    pagination_class = CustomPagination
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerialiser
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class ShoppingCartView(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """Add & delete recipe in shopping card."""

    #  !!!takes 1 positional argument but 2 were given
    #permission_classes = [IsAuthenticated, ]
    serializer_class = ShoppingCartSerializer
    queryset = Recipe.objects.all()


class DownloadShoppingCart(generics.ListAPIView):
    """Dowload shopping card."""

    permission_classes = [IsAuthenticated, ]

    def get(self, request, id, format=None):

        ingredient_list = "Cписок покупок:"
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
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
        response = HttpResponse(ingredient_list, 'Content-Type: application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file}.pdf"'
        return response