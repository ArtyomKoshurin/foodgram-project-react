# Generated by Django 4.2.5 on 2023-10-09 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("recipes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="recipes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="recipe_ingredients",
                through="recipes.IngredientsForRecipe",
                to="recipes.ingredient",
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="tag",
            field=models.ManyToManyField(related_name="recipe_tag", to="recipes.tag"),
        ),
        migrations.AddField(
            model_name="ingredientsforrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="recipes.ingredient"
            ),
        ),
        migrations.AddField(
            model_name="ingredientsforrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="recipes.recipe"
            ),
        ),
    ]
