from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from colorfield.fields import ColorField

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            db_index=True,
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug],
                            )
    color = ColorField(default='#FF0000')


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True,
                            )
    measurement_unit = models.CharField(max_length=30,
                                        )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['name', 'measurement_unit'], name='unique ingredient'),)

    # Color objects are serialized into 'rgb(#, #, #)' notation.
    # def to_representation(self, value):
    #     return "rgb(%d, %d, %d)" % (value.red, value.green, value.blue)
    #
    # # "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
    # def to_internal_value(self, data):
    #     data = data.strip('rgb(').rstrip(')')
    #     red, green, blue = [int(col) for col in data.split(',')]
    #     return Color(red, green, blue)


class Recipes(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               db_index=True,
                               )

    name = models.CharField(max_length=200,
                            unique=True,
                            db_index=True,
                            )
    image = models.ImageField(upload_to='image/')
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientsRecipe',
                                         through_fields=('recipe', 'ingredient'),
                                         blank=True,


                                         )
    tags = models.ManyToManyField('Tag', related_name='recipes',
                                  blank=True,

                                  )  #write correct
    cooking_time = models.IntegerField(validators=[MinValueValidator(1)]) #write count minut >=1
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)


class IngredientsRecipe(models.Model):
    recipe = models.ForeignKey(Recipes, related_name='all_ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='recipe_id', on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['recipe', 'ingredient'], name='unique recipe-ingredient'),)


class Subscribe(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Подписки',
                               )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'author'], name='unique follow'),)


class Favorite(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favorit_recipe',

                             )
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='favorit_user',
                                )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipes'], name='unique favorited'),)


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             )
    recipes = models.ForeignKey(Recipes,
                                on_delete=models.CASCADE,
                                related_name='shopping_user',
                                )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipes'], name='unique shopping'),)

# shopping_cart = models.ManyToManyField(Recipes, related_name='shopping_cart', blank=True, null=True)
#     кодирование картинки  BASE64
# При публикации рецепта фронтенд кодирует картинку в строку base64;
# на бэкенде её необходимо декодировать и сохранить как файл.

# Для этого будет удобно создать кастомный
# тип поля для картинки, переопределив метод сериализатора to_internal_value
#     переопределить мета по дате публикации
#  обрабатывается ошибка 404
# все поля обязательны для заполнения настроить ману то ману
# кукинтайм как выбрать мб интегерфилд
# Для сохранения ингредиентов и тегов
# рецепта потребуется переопределить методы create и update в ModelSerializer.
# Согласно спецификации, обновление рецептов должно быть реализовано через PATCH,
# значит, при редактировании все поля модели рецепта должны полностью перезаписываться.
# Используйте подходящие типы related-полей;
# для некоторых данных вам потребуется использовать SerializerMethodField.
# Во вьюсетах вам потребуется добавлять дополнительные action.
# Не забывайте о том, что для разных action сериализаторы и уровни доступа (permissions)
# могут отличаться.
# Некоторые методы, в том числе и action, могут быть похожи друг на друга.
# Избегайте дублирующегося кода.


#  можнт бвыть когда будет выдоча бюудем проверять есть ли у юзера данное ид рецепта
