from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов"""
    tags = filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.CharFilter(lookup_expr='exact')
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart', method='filter'
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited', method='filter'
    )

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(
                shopping_cart__user=self.request.user
            )
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorite__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited', )


class IngredientsFilter(filters.FilterSet):
    """Фильтр ингредиентов"""
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
