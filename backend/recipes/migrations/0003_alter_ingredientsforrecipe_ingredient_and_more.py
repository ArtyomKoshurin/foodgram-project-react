# Generated by Django 4.2.5 on 2023-10-21 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredientsforrecipe",
            name="ingredient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_for_recipe",
                to="recipes.ingredient",
            ),
        ),
        migrations.AlterField(
            model_name="ingredientsforrecipe",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredient_for_recipe",
                to="recipes.recipe",
            ),
        ),
    ]