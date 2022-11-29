from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet,
                    FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, )
router.register('tags', TagViewSet, )
router.register('recipes', RecipeViewSet, )
router.register('users', UserViewSet, )


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('recipes/<id>/favorite/', FavoriteViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'})),
    path('recipes/<id>/shopping_cart/', ShoppingCartViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'})),
]
