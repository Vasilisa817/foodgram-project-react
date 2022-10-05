from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                       ShoppingCartView, ShowSubscriptionsView, SubscribeView,
                       TagViewSet, DownloadShoppingCart)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        DownloadShoppingCart.as_view(),
        name='download_shopping_cart'
    ),
    path(
        r'recipes/<recipe_id>/shopping_cart/',
        ShoppingCartView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='shopping_cart'
    ),
    path(
        r'recipes/<recipe_id>/favorite/',
        FavoriteView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='favorite'
    ),
    path(
        r'users/<author_id>/subscribe/',
        SubscribeView.as_view({'post': 'create', 'delete': 'destroy'}),
        name='subscribe'
    ),
    path(
        'users/subscriptions/',
        ShowSubscriptionsView.as_view({'get': 'list', }),
        name='subscriptions'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
