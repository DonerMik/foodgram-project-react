from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers

from api.views import UserCustomViewSet, TagViewSet, IngredientsViewSet, RecipesViewSet

router = routers.DefaultRouter()
router.register('users', UserCustomViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)
# router.register(r'users', UserViewSet)
# router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),

    path('auth/', include('djoser.urls.authtoken')),
]



