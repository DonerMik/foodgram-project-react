from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Ingredient, IngredientsRecipe,
                            Recipes, Tag, Subscribe)

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
        return Subscribe.objects.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', required=False)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', required=False
    )

    class Meta:
        model = IngredientsRecipe
        fields = ['id', 'name', 'measurement_unit', 'amount']


class RecipesGetSerializer(serializers.ModelSerializer):
    author = UserCustomSerializer()
    image = Base64ImageField()
    ingredients = IngredientsRecipeSerializer(many=True, read_only=True,
                                              source='all_ingredients')
    tags = TagSerializer(many=True, read_only=True)
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
        if user.is_authenticated:
            if user.favorit_recipe.filter(recipes=obj).exists():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            if user.shopping_cart.filter(recipes=obj.id).exists():
                return True
        return False


class RecipesCreateUpdateSerializer(serializers.ModelSerializer):
    author = UserCustomSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = IngredientsRecipeSerializer(
        many=True, source='all_ingredients')
    tags = TagSerializer(many=True,
                         read_only=True)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time',
                  )

    def create_ingredients_recipe(self, list_ingredients, recipe,):
        ingredients_recipe = []
        for ingredient in list_ingredients:
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
        return recipe

    def validate(self, attrs):
        ingredients_data = attrs['all_ingredients']
        ingredients = []
        for ingredient in ingredients_data:
            ingredient_id = ingredient['ingredient']['id']
            if ingredient_id in ingredients:
                raise serializers.ValidationError(
                    'Ингридиент повторяется')
            ingredients.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise serializers.ValidationError(
                    'Отрицательное количество ингредиентов')
        tags = self.initial_data['tags']
        if not tags:
            raise serializers.ValidationError('Выберите тег')
        tag_set = []
        for tag in tags:
            if tag in tag_set:
                raise serializers.ValidationError('Тэг повторяется')
            tag_set.append(tag)

        cooking_time = attrs['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                'Отрицательное время')
        return attrs

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance,
         given the validated data.
        """
        user = self.context.get('request').user
        ingredients = validated_data.pop('all_ingredients')
        tags = self.initial_data.pop('tags')
        recipe = Recipes.objects.create(author=user,
                                        **validated_data,)
        recipe.tags.set(tags)
        return self.create_ingredients_recipe(ingredients, recipe)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance,
        given the validated data.
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
        instance.tags.set(tags)
        return self.create_ingredients_recipe(ingredients, instance)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipesGetSerializer(
            instance, context=context).data


class RecipesShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class UsersSubscriptionsSerializer(UserCustomSerializer):

    recipes = RecipesShortSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

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
        user = self.context.get('request').user
        return Subscribe.objects.filter(
            author=user.id, user=obj.id).exists()
