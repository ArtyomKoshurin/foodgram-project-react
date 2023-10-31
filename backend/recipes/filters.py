from django_filters import rest_framework

from .models import Ingredient, Recipe, Tag


STATUS_CHOICES = ((0, 'False'), (1, 'True'))


class IngredientFilter(rest_framework.FilterSet):
    """Фильтр для поиска ингредиента по первым символам."""

    class Meta:
        model = Ingredient
        fields = {'name': ['startswith'], }


class IdToNameFilter(rest_framework.BaseInFilter, rest_framework.CharFilter):
    pass


class RecipeFilter(rest_framework.FilterSet):
    """Фильтр рецептов по тегам, подпискам вхождению
    в избранное и список покупок."""
    author = IdToNameFilter(field_name='author__username', lookup_expr='exact')
    tag = rest_framework.ModelMultipleChoiceFilter(
        field_name='tag__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
        )
    # is_favourited = rest_framework.Choice

    class Meta:
        model = Recipe
        fields = ['author', 'tag', 'is_favorited', 'is_in_shopping_cart']
