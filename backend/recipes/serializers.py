import base64

from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import Tag, Ingredient, IngredientsForRecipe, Recipe
from users.serializers import UserInfoSerializer


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
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    cooking_time = serializers.IntegerField(required=True)
    tag = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = IngredientForRecipeSerializer(many=True)
    image = Base64ImageField()
    author = UserInfoSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'tag', 'ingredients', 'cooking_time',
                  'description', 'image')

    def validate(self, data):
        """Валидация создания рецепта - проверяет наличие
        ингредиентов, изображения и тегов."""
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                "Нужно добавить ингредиенты в рецепт."
            )
        tags = self.initial_data.get('tag')
        if not tags:
            raise serializers.ValidationError(
                "Необходимо указать хотя бы один тег."
            )
        image = self.initial_data.get('image')
        if not image:
            raise serializers.ValidationError(
                "К рецепту необходимо добавить фото."
            )
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tag')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tag.set(tags)
        for ingredient in ingredients:
            IngredientsForRecipe.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                portion=ingredient.get('portion')
            )
        return recipe
