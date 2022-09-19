from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator,
                                    validate_slug)
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Имя тега',
                            max_length=200,
                            unique=True,
                            db_index=True,
                            )
    slug = models.SlugField(verbose_name='Поле slug',
                            unique=True,
                            max_length=50,
                            validators=[validate_slug],
                            )
    color = ColorField(verbose_name='Цвет',
                       default='#FF0000')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Имя ингредиента',
                            max_length=200,
                            db_index=True,
                            )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=30,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (models.UniqueConstraint(
            fields=['name', 'measurement_unit'], name='unique ingredient'),)


class Recipes(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               db_index=True,
                               )
    name = models.CharField(verbose_name='Навзание рецепта',
                            max_length=200,
                            unique=True,
                            db_index=True,
                            )
    image = models.ImageField(upload_to='image/',
                              verbose_name='Изображение')
    text = models.TextField(verbose_name='Содержание')
    ingredients = models.ManyToManyField(
        Ingredient, blank=False,
        null=False,
        verbose_name='Ингридиенты',
        through='IngredientsRecipe',
        through_fields=('recipe', 'ingredient'),
    )
    tags = models.ManyToManyField('Tag', related_name='recipes',
                                  blank=True,
                                  )
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)],
                                       verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публткации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        related_name='all_ingredients',
        on_delete=models.CASCADE,
        )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe_id',
        on_delete=models.CASCADE)
    amount = models.IntegerField(
        validators=[MinValueValidator(1)])

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['recipe', 'ingredient'], name='unique recipe-ingredient'),)
        verbose_name = 'Ингридиенты рецепта'
        verbose_name_plural = 'Ингридиенты рецепта'


class Subscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             blank=True,
                             null=True
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Подписки',
                               blank=True,
                               null=True
                               )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'author'], name='unique follow'),)
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorit_recipe',
                             verbose_name='пользователь',
                             blank=True,
                             null=True
                             )
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='favorit_user',
                                verbose_name='Рецепт',
                                blank=True,
                                null=True
                                )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipes'], name='unique_favorited'),)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             blank=True,
                             null=True
                             )
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='shopping_user',
                                blank=True,
                                null=True
                                )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipes'], name='unique shopping'),)
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
