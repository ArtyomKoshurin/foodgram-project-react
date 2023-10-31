from django_filters import rest_framework

from .models import Ingredient, Recipe, Tag


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр для поиска ингредиента по первым символам."""

    class Meta:
        model = Ingredient
        fields = {'name': ['startswith'], }


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр рецептов по тегам, подпискам вхождению
    в избранное и список покупок."""
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
        )
    tag = rest_framework.ModelMultipleChoiceFilter(
        field_name='tag__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
        )
    is_favorited = rest_framework.BooleanFilter(
        method='filter_is_favorited'
        )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='filter_is_in_shopping_cart'
        )

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        if value:
            return Recipe.objects.filter(
                favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipe.objects.none()
        if value:
            return Recipe.objects.filter(
                shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tag', 'is_favorited', 'is_in_shopping_cart']
