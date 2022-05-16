from django.db import models
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    validate_slug)
from colorfield.fields import ColorField


class Recipes(models.Model):
    author = models.ForeignKey('User',
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Рецепты',)

    name = models.CharField(max_length=200,
                            unique=True,
                            db_index=True,
                            )
    image = models.ImageField(upload_to='upload_image')
    text = models.TextField()
    ingredients = models.ManyToManyField() #write correct
    tags = models.ManyToManyField()  #write correct
    cooking_time = models.IntegerField() #write count minut >=1
# все поля обязательны для заполнения настроить ману то ману
# кукинтайм как выбрать мб интегерфилд
#  имэйдж тоже мб поле бинарное


class Tag(models.Model):
    name = models.CharField(max_length=200,
                            unique=True,
                            db_index=True,
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug],
                            )
    color = ColorField(default='#FF0000') # модельфильд создать сделать хекс


class Ingredient(models.Model):
    name_ingr = models.CharField(max_length=200,
                                 unig=True,
                                 db_index=True,
                                 )
    count = models.IntegerField() # можно валидаторы что нет отриц

    unit = models.Choices() #подумать что можно сделать с ед измерения






