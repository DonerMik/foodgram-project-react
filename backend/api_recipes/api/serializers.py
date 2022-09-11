from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientsRecipe, Recipes, Tag

User = get_user_model()


class UserCustomSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        obj_user = User.objects.get(username=user)
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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipesSerializer(serializers.ModelSerializer):
    author = UserCustomSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientsRecipeSerializer(
        read_only=True,
        many=True,
        source='all_ingredients')
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
        username = self.context.get('request').user
        if username.is_authenticated:
            obj_user = User.objects.get(username=username)
            if obj_user.favorit_recipe.filter(recipes=obj.id).exists():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            obj_user = User.objects.get(username=user)
            if obj_user.shopping_cart.filter(recipes=obj.id).exists():
                return True
        return False

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredients = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients:
                raise serializers.ValidationError({
                    'ingredients': 'Ингридиент повторяется'
                })
            ingredients.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError({
                    'amount': 'Отрицательное количество ингредиентов'
                })

        tags = data.get('tags')
        if not tags:
            raise serializers.ValidationError({
                'tags': 'Выберите тег'
            })
        tags = []
        for tag in tags:
            if tag in tags:
                raise serializers.ValidationError({
                    'tags': 'Тэг повторяется'
                })
            tags.append(tag)

        cooking_time = data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError({
                'cooking_time': 'Отрицательное время'
            })
        return data

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance,
         given the validated data.
        """
        user = self.context.get('request').user
        author = User.objects.get(username=user)
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipes.objects.create(author=author, **validated_data)
        ingredients_recipe = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            recipe_ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient_amount = ingredient['amount']
            ingredients_recipe.append(IngredientsRecipe(
                recipe=recipe,
                ingredient=recipe_ingredient,
                amount=ingredient_amount
            )
            )
        IngredientsRecipe.objects.bulk_create(ingredients_recipe)
        for tag in tags:
            recipe.tags_set.set(tag)
        return recipe

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance,
        given the validated data...
        """
        ingredients = self.initial_data.pop('ingredients')
        tags = self.initial_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time)
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
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed', 'recipes',
                  'recipes_count')

    def get_recipes_count(self, obj):
        author = self.context.get('request').user
        recipes_count = author.recipes.all().count()
        return recipes_count

    def get_is_subscribed(self, obj):
        obj_user = self.context.get('request').user
        return obj_user.follower.filter(author=obj.id).exists()
