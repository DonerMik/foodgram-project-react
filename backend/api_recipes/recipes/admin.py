from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientsRecipe, Recipes,
                            ShoppingCart, Subscribe, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


# @admin.register(Favorite)
# class FavoriteAdmin(admin.ModelAdmin):
#     list_display = ('user', 'recipe',)
#     list_filter = ('user', 'recipe',)


class IngredientInline(admin.TabularInline):
    model = Recipes.ingredients.through


class IngredintsAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'add_favorite')
    search_fields = ('author', 'name', 'tags')
    exclude = ('ingredients',)
    inlines = [
        IngredientInline
    ]
    ordering = ('-id',)

    def add_favorite(self, obj):
        return obj.favorit_user.count()
    add_favorite.short_description = 'Добавлено в избранное'


admin.site.register(Favorite)
admin.site.register(Subscribe)
admin.site.register(ShoppingCart)
admin.site.register(IngredientsRecipe)

admin.site.site_title = 'Админ-панель сайта Foodgram'
admin.site.site_header = 'Админ-панель сайта Foodgram'
