from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets

from .filters import IngredientsFilter, RecipeFilter
from .permissions import IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
from .serializers import (CreateRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вывод рецептов """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorModeratorAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """ Вывод тегов """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вывод ингредиентов """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filterset_class = IngredientsFilter
