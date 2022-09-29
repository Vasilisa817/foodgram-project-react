from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartView, ShowSubscriptionsView, SubscribeView,
                    TagViewSet, DownloadShoppingCart)

app_name = 'api'

router = DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients') #ok
router.register('recipes', RecipeViewSet, basename='recipes') #ok
router.register('tags', TagViewSet, basename='tags') #ok

urlpatterns = [
    path(
        'recipes/download_shopping_cart/', #ok
        DownloadShoppingCart.as_view(),
        name='download_shopping_cart'
    ),
    path(
        'recipes/<int:id>/shopping_cart/', #takes 1 positional argument but 2 were given
        ShoppingCartView,
        name='shopping_cart'
    ),
    path(
        'recipes/<int:id>/favorite/', #takes 1 positional argument but 2 were given
        FavoriteView,
        name='favorite'
    ),
    path(
        'users/<author_id>/subscribe/',
        SubscribeView,
        name='subscribe'
    ),
    path(
        'users/subscriptions/', #takes 1 positional argument but 2 were given
        ShowSubscriptionsView,
        name='subscriptions'
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')), #ok
    path('', include(router.urls)),
]