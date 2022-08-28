from api.views import (IngredientsViewSet, RecipesViewSet, TagViewSet,
                       UserCustomViewSet)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserCustomViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),

    path('auth/', include('djoser.urls.authtoken')),
]



