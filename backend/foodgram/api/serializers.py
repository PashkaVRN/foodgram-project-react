from rest_framework import serializers
from recipes.models import (Tag , Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Favorite)
from users.models import User, Follow


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра тегов"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор просмотра ингридиентов"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class UserCreateSerializer(serializers.UserCreateSerializer):
    """Сериализатор создания юзера"""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name', 'password'
                  )
