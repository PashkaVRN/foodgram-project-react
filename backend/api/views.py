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
from recipes.models import (Ingredient, IngredientRecipe, Recipe,
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
        if self.request.method in ('POST', 'PATH'):
            return RecipeReadSerializer
        return CreateRecipeSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        ingredients = serializer.validated_data.pop('ingredients')
        tags = serializer.validated_data.pop('tags')
        IngredientRecipe.objects.filter(recipes=instance).delete()
        Recipe.objects.filter(recipes=instance).delete()
        instance.name = serializer.validated_data.pop('name')
        instance.text = serializer.validated_data.pop('text')
        if serializer.validated_data.get('image') is not None:
            instance.image = serializer.validated_data.pop('image')
        instance.cooking_time = serializer.validated_data.pop('cooking_time')
        instance.tags.set(tags)
        for ing in ingredients:
            IngredientRecipe.objects.bulk_create([IngredientRecipe(
                recipes=instance,
                amount=ing['amount'],
                ingredients=ing['ingredients'])])
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(RecipeViewSet, self).get_serializer_context()
        context.update({'request': self.request})
        return context

    def create(self, request, *args, **kwargs):
        request.data['author'] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingredients = serializer.validated_data.pop('ingredients')
        instance = serializer.save(author=request.user)
        for ing in ingredients:
            IngredientRecipe.objects.bulk_create([IngredientRecipe(
                ingredients=ing['ingredients'],
                recipes=instance,
                amount=ing['amount'])])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(serializer.validated_data)


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
