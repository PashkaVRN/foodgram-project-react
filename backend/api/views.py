from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorModeratorAdminOrReadOnly
from recipes.models import (Ingredient, Recipe,
                            Tag)
from .serializers import (CreateRecipeSerializer, IngredientSerializer,
                          RecipeReadSerializer,
                          SubscribeListSerializer, TagSerializer,
                          UserSerializer)
from users.models import Follow, User


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вывод ингредиентов """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = CustomPagination
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    """ Вывод тегов """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """ Вывод работы с рецептами """
    queryset = Recipe.objects.all()
    serializer_class = CreateRecipeSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATH',):
            return RecipeReadSerializer
        return CreateRecipeSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = SubscribeListSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(
                Follow, user=user, author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeListSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
