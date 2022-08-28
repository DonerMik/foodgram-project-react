from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientsRecipe, Recipes, Tag
from rest_framework import serializers

User = get_user_model()


class UserCustomSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        username = self.context.get('request').user
        if username.is_authenticated:
            obj_user = User.objects.get(username=username)
            if obj_user.follower.filter(author=obj.id).exists():
                return True
        return False



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = IngredientsRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']

    def get_id(self, obj):
        return obj.ingredient.id

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
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time',
                  )

    def get_is_favorited(self, obj):

        # наверно нужно будет перенастрить тут так сбе енаписан и непонятно
        username = self.context.get('request').user
        print('FFFFFFFFFFFFFFFFFFFFFFF')
        print(self.context['request'].user.is_authenticated)
        if username.is_authenticated:
            obj_user = User.objects.get(username=username)
            if obj_user.favorit_recipe.filter(recipes=obj.id).exists():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        # наверно нужно будет перенастрить тут так сбе енаписан и непонятно
        username = self.context.get('request').user
        print('FFFFFFFFFFFFFFFFFFFFFFF')
        print(self.context['request'].user.is_authenticated)
        if username.is_authenticated:
            obj_user = User.objects.get(username=username)
            if obj_user.shopping_cart.filter(recipes=obj.id).exists():
                return True
        return False

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
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


class RecipesShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class UsersSubscriptionsSerializer(UserCustomSerializer):

    recipes = RecipesShortSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        # user = self.context.get('request').user
        author = User.objects.get(pk=obj.pk)
        recipes_count = author.recipes.all().count()
        return recipes_count

    def get_is_subscribed(self, obj):
        # наверно нужно будет перенастрить тут так сбе енаписан и непонятно
        # username = obj.username
        # user = self.request.user
        obj_user = User.objects.get(pk=obj.pk)
        if obj_user.follower.filter(author=obj.id).exists():
            return True
        return False

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
