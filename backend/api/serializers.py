from djoser.serializers import UserCreateSerializer
from rest_framework import serializers, validators
from django.shortcuts import get_object_or_404

from api.field import Base64ImageField
from users.models import User, Follow
from recipes.models import (
    Tag, Recipe, Ingredient,
    IngredientRecipe, Favorite,
    ShoppingCart, RecipeTag,
)


class CustomUserCreateSerializer(UserCreateSerializer):
    """Serializer for create user."""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class UsersManageSerializer(serializers.ModelSerializer):
    """Serializer for model User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for model Tags."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for model Ingredient."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )
        read_only_fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Seralizer for output the amount of ingredients."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')


class RecipeSerialiser(serializers.ModelSerializer):
    """Serializer for view recipe."""

    tags = TagSerializer(many=True, read_only=True)
    author = UsersManageSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientAmountSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """Serializer for add ingredient in recipe. """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Serializer for create & update recipe."""

    author = UsersManageSerializer(read_only=True)
    ingredients = AddIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    image = Base64ImageField(max_length=10000, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        ]

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        _list_of_ingridients = []
        for i in ingredients:
            amount = i['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Количество ингредиентов должно быть больше 0!'
                })
            if i['id'] in _list_of_ingridients:
                raise serializers.ValidationError({
                    'ingredient': 'Ингредиенты должны быть уникальными!'
                })
            _list_of_ingridients.append(i['id'])
        return self.initial_data

    def create_related_objects(self, recipe, ingredients, tags):
        ingredients_list = list()
        tags_list = list()
        for ingredient in ingredients:
            ingr_object = IngredientRecipe(
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient['id']
                ),
                recipe=recipe,
                amount=ingredient['amount']
            )
            ingredients_list.append(ingr_object)
        for tag in tags:
            tag_object = RecipeTag(
                recipe=recipe,
                tag=get_object_or_404(Tag, id=tag)
            )
            tags_list.append(tag_object)

        IngredientRecipe.objects.bulk_create(ingredients_list)
        RecipeTag.objects.bulk_create(tags_list)

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        recipe.save()
        self.create_related_objects(recipe, ingredients, tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.id).update(**validated_data)
        recipe = Recipe.objects.get(id=instance.id)
        IngredientRecipe.objects.filter(recipe=recipe).delete()
        RecipeTag.objects.filter(recipe=recipe).delete()
        self.create_related_objects(recipe, ingredients, tags)
        return recipe

    def to_representation(self, instance):
        return RecipeSerialiser(instance, context={
            'request': self.context.get('request')
        }).data


class ShowFavoriteSerializer(serializers.ModelSerializer):
    """Serializer for display favorites recipes."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer for the shopping list."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowFavoriteSerializer(instance.recipe, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for favorites recipes."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShowFavoriteSerializer(instance.recipe, context=context).data


class ShowSubscriptionsSerializer(serializers.ModelSerializer):
    """Serailizer for display user subscriptions."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params.get('recipes_limit')
        if limit:
            recipes = recipes[:int(limit)]
        return ShowFavoriteSerializer(
            recipes, many=True, context={'request': request}).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for model Follow."""

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
            ),
        )

    def to_representation(self, instance):
        return ShowSubscriptionsSerializer(instance.author, context={
            'request': self.context.get('request')
        }).data
