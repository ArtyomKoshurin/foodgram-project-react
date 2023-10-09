from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        max_length=124,
        unique=True,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(max_length=124)
    measure_unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        CustomUser,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=254)
    image = models.ImageField(
        upload_to='recipes/images/',
        default=None
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsForRecipe',
        related_name='recipe_ingredients'
        )
    tag = models.ManyToManyField(Tag, related_name='recipe_tag')
    cooking_time = models.PositiveIntegerField()
    is_favourite = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class IngredientsForRecipe(models.Model):
    """Вспомогательная модель для добавления ингредиентов в рецепт."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    portion = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'
