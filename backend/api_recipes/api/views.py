from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from api.utils import get_pdf
from recipes.models import (Favorite, Ingredient, Recipes,
                            ShoppingCart, Subscribe, Tag)
from api.filter import IngredientsFilter, RecipesFilter
from api.paginator import CustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipesSerializer,
                             RecipesShortSerializer, TagSerializer,
                             UserCustomSerializer,
                             UsersSubscriptionsSerializer)

User = get_user_model()


class UserCustomViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCustomSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    @action(detail=False, pagination_class=CustomPagination)
    def subscriptions(self, request):
        obj_user = request.user
        subscribers = obj_user.follower.all()
        subscribers = User.objects.filter(
            id__in=(subs.author.pk for subs in subscribers))
        serializer = UsersSubscriptionsSerializer(
            subscribers, context={'request': request}, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

    @action(detail=True, methods=['post', 'delete'],
            pagination_class=CustomPagination)
    def subscribe(self, request, id=None):
        user = request.user
        sub_user = get_object_or_404(User, id=id)
        serializer = UsersSubscriptionsSerializer(
            user, context={'request': request})
        if request.method == "POST":
            Subscribe.objects.create(user=user,
                                     author=sub_user)
            return Response(serializer.data)
        Subscribe.objects.get(user=user,
                              author=sub_user).delete()
        return Response('удален')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    permission_classes = [AllowAny]


class CreateOrDeleteMixIn:
    ''' Миксин создает или удаляет объект одного класса.
    Возвращает Response'''

    @staticmethod
    def create_or_delete_obj(self, request, user, obj2, cls, serializer):
        '''Метод создает объект с двумя полями.
        Первое из которых поле user'''
        if request.method == "POST":
            cls.objects.create(user, obj2)
            return Response(serializer.data)
        cls.objects.get(user, obj2).delete()
        return Response('удален')

    class Meta:
        abstract = True


class RecipesViewSet(viewsets.ModelViewSet, CreateOrDeleteMixIn):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipesFilter
    permission_classes = [AllowAny]

    @action(detail=False, permission_classes=[IsAuthenticated],)
    def download_shopping_cart(self, request):
        return get_pdf(request)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        return self.create_or_delete_obj(
            request, user, recipe, ShoppingCart, serializer)
        # if request.method == "POST":
        #     ShoppingCart.objects.create(user=user,
        #                                 recipes=recipe)
        #
        #     return Response(serializer.data)
        # ShoppingCart.objects.get(user=user,
        #                          recipes=recipe).delete()
        # return Response('удален')

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated],
            filterset_class=RecipesFilter,
            pagination_class=CustomPagination)
    def favorite(self, request, pk=None):
        user = request.user
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe,
                                            context={'request': request})
        return self.create_or_delete_obj(
            request, user, recipe, Favorite, serializer)
        # if request.method == "POST":
        #     Favorite.objects.create(user=user,
        #                             recipes=recipe)
        #
        #     return Response(serializer.data)
        # Favorite.objects.get(user=user,
        #                      recipes=recipe).delete()
        # return Response('удален')
