from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, IngredientRecipe


class IngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 3


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'cooking_time')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientInline,)


class IngredientAdmin(admin.ModelAdmin):
    """ Админ панель управление ингридиентами """
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """ Админ панель управление тегами """
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', )
    empty_value_display = '-пусто-'


# class RecipeAdmin(admin.ModelAdmin):
#     """ Админ панель управление рецептами """
#     list_display = ('author', 'name', 'cooking_time')
#     search_fields = ('name', 'author', 'tags')
#     list_filter = ('author', 'name', 'tags')
#     empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    """ Админ панель управление подписками """
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    """ Админ панель списка покупок """
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user', )
    empty_value_display = '-пусто-'


admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
