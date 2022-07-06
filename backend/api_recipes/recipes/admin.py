
from django.contrib import admin

# from api.views import Ingredients
from .models import Tag, Recipes, IngredientsRecipe, Subscribe, Favorite, ShoppingCart, Ingredient


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'color')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class RecipesAdmin(admin.ModelAdmin):
    # list_display = ('pk', 'author', 'name',  'image', 'ingredients',
    #                 'tags', 'cooking_time', 'pub_date',)
    list_display = ('author', 'name', 'add_favorite',)

    search_fields = ('author', 'name', 'tags')
    list_filter = ('author', 'name',)
    empty_value_display = '-пусто-'

    def add_favorite(self, obj):
        return obj.favorites.count()
    add_favorite.short_description = 'Добавлено в избранное'


class IngredientsRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('ingredient',)
    empty_value_display = '-пусто-'



class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')
    search_fields = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(IngredientsRecipe, IngredientsRecipeAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
