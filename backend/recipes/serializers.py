import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import Tag, Ingredient, IngredientsForRecipe


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measure_unit')


class IngredientForRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления ингредиента в рецепт."""
    id = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientsForRecipe
        fields = ('id', 'portion')


class RecipeCreationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецепта"""
