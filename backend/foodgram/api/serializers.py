from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag, TagRecipe)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователя"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return all(
            (request is not None,
             not request.user.is_anonymous,
             Follow.objects.filter(
                 user=request.user, author=obj
             ).exists())
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name',
            'last_name', 'password')


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра ингридиентов"""
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор связи ингридиентов и рецепта"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
                            source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра рецепта"""
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(
        method_name='get_is_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        method_name='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time'
                  )

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj).exists()


class RecipeListSubscribeSerializer(serializers.ModelSerializer):
    """Вывод рецептов в подписках """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок """

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]

    def to_representation(self, instance):
        return RecipeListSubscribeSerializer(instance.recipe,
                                             context=self.context).data


class AddIngredientRecipeSerializer(serializers.ModelSerializer):
    """ Сериализатор добавление ингридиентов в рецепт """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избраных рецептов """

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')


class SubscribeListSerializer(serializers.ModelSerializer):
    """Сериализатор для получения подписок """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context('request')
        if Follow.objects.filter(user=request.user, author=obj).exists():
            return True
        return False

    def get_recipes(self, obj):
        request = self.context('request')
        if request.user.is_anonymous:
            return False
        recipes = Recipe.objects.filter(author=obj)
        limit = request.query_params['recipes_limit']
        if limit:
            recipes = recipes[:int(limit)]
        return RecipeSerializer(
            recipes, many=True, context=self.context).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class AmountIngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор добавления ингредиента с указанием количества в рецепт """
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор создания, редактирования рецепта """
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountIngredientInRecipeSerializer(many=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time'
                  )

    def get_ingredients(self, obj):
        record = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(record, many=True).data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        author = self.context.get('request').user
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients_data:
            ingredient_model = ingredient['id']
            amount = ingredient['amount']
            IngredientRecipe.objects.create(
                ingredient=ingredient_model,
                recipe=recipe,
                amount=amount
            )
        for tag in tags_data:
            TagRecipe.objects.create(recipe=recipe, tag=tag)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredient_data = validated_data.pop('ingredients')
        TagRecipe.objects.filter(recipe=instance).delete()
        for tag in tags_data:
            TagRecipe.objects.create(
                recipe=instance,
                tag=tag
            )
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for new_ingredient in ingredient_data:
            IngredientRecipe.objects.create(
                ingredient=new_ingredient['id'],
                recipe=instance,
                amount=new_ingredient['amount']
            )
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.save()
        return instance
