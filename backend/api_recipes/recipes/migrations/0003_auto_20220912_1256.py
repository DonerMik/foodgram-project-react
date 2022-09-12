# Generated by Django 3.2.13 on 2022-09-12 09:56

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранные'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='ingredientsrecipe',
            options={'verbose_name': 'Ингридиенты рецепта', 'verbose_name_plural': 'Ингридиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipes',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'Подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorit_user', to='recipes.recipes', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorit_recipe', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=30, verbose_name='Единица измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='Имя ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='cooking_time',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='image',
            field=models.ImageField(upload_to='image/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientsRecipe', to='recipes.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='name',
            field=models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Навзание рецепта'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публткации'),
        ),
        migrations.AlterField(
            model_name='recipes',
            name='text',
            field=models.TextField(verbose_name='Содержание'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(db_index=True, max_length=200, unique=True, verbose_name='Имя тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), 'Enter a valid “slug” consisting of letters, numbers, underscores or hyphens.', 'invalid')], verbose_name='Поле slug'),
        ),
    ]
