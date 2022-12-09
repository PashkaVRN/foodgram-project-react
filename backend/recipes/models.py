from colorfield.fields import ColorField
from django.conf import settings
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User


class Ingredient(models.Model):
    """ Модель ингридиентов. """
    name = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_RECIPES,
        verbose_name='Название ингридиента',
        db_index=True
    )
    measurement_unit = models.CharField(
        max_length=settings.LENGTH_OF_FIELDS_RECIPES,
        verbose_name='Еденицы измерения'
    )

    class Meta():
        verbose_name = 'Ингридиенты'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """ Модель тегов."""
    name = models.CharField(
        verbose_name='Название тега',
        max_length=settings.LENGTH_OF_FIELDS_RECIPES,
        db_index=True,
        unique=True
    )
    color = ColorField(
        verbose_name='HEX-код',
        format='hex',
        max_length=7,
        unique=True,
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                message='Проверьте вводимый формат',
            )
        ],
    )
    slug = models.SlugField(
        max_length=settings.LENGTH_OF_FIELDS_RECIPES,
        verbose_name='Slug',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель рецептов. """
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=settings.LENGTH_OF_FIELDS_RECIPES,
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        verbose_name='Изображение'
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки',
        validators=[MinValueValidator(
            1, message='Время приготовления не менее 1 минуты!'
        ), MaxValueValidator(
            1441, message='Время приготовления не более 24 часов!'
        )]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavoriteShoppingCart(models.Model):
    """ Связывающая модель списка покупок и избранного. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='%(app_label)s_%(class)s_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} :: {self.recipe}'


class Favorite(FavoriteShoppingCart):
    """ Модель добавление в избраное. """

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(FavoriteShoppingCart):
    """ Модель списка покупок. """

    class Meta(FavoriteShoppingCart.Meta):
        default_related_name = 'shopping_list'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class IngredientRecipe(models.Model):
    """ Ингридиенты рецепта. """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredienttorecipe'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество ингредиента'
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return (
            f'{self.ingredient.name} :: {self.ingredient.measurement_unit}'
            f' - {self.amount} '
        )
