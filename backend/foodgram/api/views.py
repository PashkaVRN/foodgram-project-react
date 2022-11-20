from rest_framework import viewsets
from recipes.models import (Recipe, Tag, Ingredient, )
from .permissions import IsAuthorModeratorAdminOrReadOnly, IsAdminOrReadOnly
from .filters import RecipeFilter, IngredientsFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (RecipeSerializer, TagSerializer,
                          IngredientSerializer, CreateRecipeSerializer, )


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление рецептов."""

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
    """Представление тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Отображение ингредиентов. """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filterset_class = IngredientsFilter
