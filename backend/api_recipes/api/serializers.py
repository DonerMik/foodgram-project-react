import base64
from datetime import datetime
from django.forms import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from recipes.models import Tag, Ingredient, Recipes, IngredientsRecipe
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
User = get_user_model()


# class Image(serializers.Field):
#     def to_representation(self, value):
#         return value
#
#     def to_internal_value(self, value):
#         # name_file = data[-20:]
#
#         image_code = value.split('base64,')[1]
#
#         # with open(f'{datetime.now()}.png', 'wb', encoding='utf8') as w:
#         image = base64.b64decode(image_code)
#            w.write(image)
#         # fh = open('asd.png', 'wb')
#         # with open(f"{data}.jpg", "wb", encoding="ascii", errors='ignore') as f:
#         #     f.write(data.decode('base64'))
#         # return f'{data}.jpg'
#         return image


class UserCustomSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        # наверно нужно будет перенастрить тут так сбе енаписан и непонятно
        username = self.context.get('request').user
        # user = self.request.user
        obj_user = User.objects.get(username=username)
        if obj_user.follower.filter(author=obj.id).exists():
            return True
        return False
    # нужно добвать если связь есть то Тру иначе фолс
    # достать юзера нуждно


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')

# Тут будет какае т дичь нужно разобраться и углубиться со связами и тд


class IngredientsRecipeSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientsRecipe
        fields = ['ingredient', 'name', 'measurement_unit', 'amount']

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipesSerializer(serializers.ModelSerializer):
    author = UserCustomSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientsRecipeSerializer(read_only=True,
                                              many=True, source='all_ingredients')
    tags = TagSerializer(many=True,
                         read_only=True)
    # subscribe = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',
                  )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        author = User.objects.get(username=user)
        if obj.favorit_user.filter(user=author).exists():
        # if author in obj.favorit_user.all():
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        author = User.objects.get(username=user)
        if obj.shopping_user.filter(user=author).exists():

            return True
        return False


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        # if 'ingredients' not in self.initial_data:
        user = self.context.get('request').user
        author = User.objects.get(username=user)
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipes.objects.create(author=author, **validated_data)
        # дописать елси пусто вернуть
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            recipe_ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient_amount = ingredient['amount']
            IngredientsRecipe.objects.create(
                recipe=recipe,
                ingredient=recipe_ingredient,
                amount=ingredient_amount
            )
        for tag in tags:
            tag_recipe = Tag.objects.get(id=tag)
            recipe.tags.add(tag_recipe)
        return recipe

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        # user = self.context.get('request').user
        # author = User.objects.get(username=user)
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        IngredientsRecipe.objects.filter(recipe=instance).delete()
        instance.tags.clear()
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            recipe_ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient_amount = ingredient['amount']

            IngredientsRecipe.objects.create(
                recipe=instance,
                ingredient=recipe_ingredient,
                amount=ingredient_amount
            )
        for tag in tags:
            tag_recipe = Tag.objects.get(id=tag)
            instance.tags.add(tag_recipe)
        instance.save()
        return instance




    # def create(self, validated_data):
    #     # Если в исходном запросе не было поля achievements
    #     if 'achievements' not in self.initial_data:
    #         # То создаём запись о котике без его достижений
    #         cat = Cat.objects.create(**validated_data)
    #         return cat
    #
    #     # Иначе делаем следующее:
    #     # Уберём список достижений из словаря validated_data и сохраним его
    #     achievements = validated_data.pop('achievements')
    #     # Сначала добавляем котика в БД
    #     cat = Cat.objects.create(**validated_data)
    #     # А потом добавляем его достижения в БД
    #     for achievement in achievements:
    #         current_achievement, status = Achievement.objects.get_or_create(
    #             **achievement)
    #         # И связываем каждое достижение с этим котиком
    #         AchievementCat.objects.create(
    #             achievement=current_achievement, cat=cat)
    #     return cat
# class TitleSerializerPostPatch(serializers.ModelSerializer):
#     description = serializers.CharField(required=False)
#     genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
#                                          many=True,
#                                          slug_field='slug')
#     category = serializers.SlugRelatedField(queryset=Category.objects.all(),
#                                             slug_field='slug')
#
#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'description',
#                   'genre', 'category')
#
#
# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(`/
#         read_only=True, slug_field='username'
#     )
#     title = serializers.SlugRelatedField(
#         read_only=True, slug_field='name'
#     )
#
#     class Meta:
#         model = Review
#         fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
#
#     def validate(self, attrs):
#         method = self.context.get('request').method
#         if method != 'POST':
#             return super().validate(attrs)
#
#         title_id = self.context.get('view').kwargs['title_id']
#         author = self.context.get('request').user
#         if Review.objects.filter(
#                 author=author, title_id=title_id
#         ).exists():
#             raise ValidationError(
#                 'Нельзя дважды написать отзыв на одно произведение')
#         return super().validate(attrs)
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username'
#     )
#
#     class Meta:
#         model = Comment
#         fields = ('id', 'text', 'author', 'pub_date')
#

# class UserSignupSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())],
#     )
#     username = serializers.CharField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())],
#     )
#
#     def validate_username(self, value):
#         if value == 'me':
#             raise serializers.ValidationError('Недопустимое имя пользователя')
#
#         return value


# class TokenSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     confirmation_code = serializers.CharField(required=True)

#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = (
#             'username', 'email', 'first_name', 'last_name', 'bio', 'role'
#         )
