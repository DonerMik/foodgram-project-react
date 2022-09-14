from django_filters import (CharFilter, FilterSet,
                            ModelMultipleChoiceFilter, NumberFilter)

from recipes.models import Ingredient, Recipes, Tag


class RecipesFilter(FilterSet):
    author = NumberFilter(field_name='author__id')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    is_favorited = NumberFilter(method='filter_is_favorited')
    is_in_shopping_cart = NumberFilter(method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        print(value)
        if not value:
            return queryset
        if value:
            favorits = self.request.user.favorit_recipe.all()
            queryset = queryset.filter(
                pk__in=(favorite.recipes.pk for favorite in favorits))
            return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not self.request.user.is_anonymous:
            shopping_user = user.shopping_cart.all()
            return queryset.filter(
                id__in=(i.recipes.pk for i in shopping_user))
        return queryset

    class Meta:
        model = Recipes
        fields = ['is_favorited', 'is_in_shopping_cart', 'author', 'tags']


class IngredientsFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ['name', ]
