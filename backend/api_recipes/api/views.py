from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.utils import get_pdf
from recipes.models import (Favorite, Ingredient, IngredientsRecipe, Recipes,
                            ShoppingCart, Subscribe, Tag)
from api.filter import IngredientsFilter, RecipesFilter
from api.paginator import CustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipesSerializer,
                             RecipesShortSerializer, TagSerializer,
                             UserCustomSerializer, UsersSubscriptionsSerializer)

User = get_user_model()

class CreateOrDeleteMixIn:
    ''' Миксин создает или удаляет объект одного класса.
    Возвращает Response'''

    @staticmethod
    def create_or_delete_obj(self, request, cls,
                             serializer, obj_2):
        '''Функция создает модели с двумя полями.
        Первое из которых поле user'''
        sub_user = User.objects.get_objects_or_404(id=id)
        serializer = serializer(request.user)
        if request.method == "POST":
            cls.objects.create(request.user, obj_2)
            return Response(serializer.data)
        cls.objects.get(request.user, sub_user).delete()
        return Response('serializer.errors, удален')
#вставить и обработать миксин
    class Meta:
        abstract = True


class UserCustomViewSet(UserViewSet, CreateOrDeleteMixIn):
    queryset = User.objects.all()
    serializer_class = UserCustomSerializer
    pagination_class = CustomPagination

    @action(detail=False)
    def subscriptions(self, request):
        obj_user = request.user
        serializer = UsersSubscriptionsSerializer(obj_user)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):

        obj_user = request.user
        sub_user = User.objects.get_objects_or_404(id=id)
        serializer = UsersSubscriptionsSerializer(obj_user)
        if request.method == "POST":
            Subscribe.objects.create(user=obj_user,
                                     author=sub_user)
            return Response(serializer.data)
        Subscribe.objects.get(user=obj_user,
                              author=sub_user).delete()
        return Response('serializer.errors, удален')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    permission_classes = [AllowAny]


class RecipesViewSet(viewsets.ModelViewSet, CreateOrDeleteMixIn):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RecipesFilter
    permission_classes = [AuthorOrReadOnly]

    @action(detail=False, permission_classes=[IsAuthenticated],)
    def download_shopping_cart(self, request):
        return get_pdf()




    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.create_or_delete_obj()
        obj_user = request.user
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        if request.method == "POST":
            ShoppingCart.objects.create(user=obj_user,
                                        recipes=recipe)

            return Response(serializer.data)
        ShoppingCart.objects.get(user=obj_user,
                                 recipes=recipe).delete()
        return Response('serializer.errors, удален')

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        obj_user = request.user(self, request)
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        if request.method == "POST":
            Favorite.objects.create(user=obj_user,
                                    recipes=recipe)

            return Response(serializer.data)
        Favorite.objects.get(user=obj_user,
                                 recipes=recipe).delete()
        return Response('serializer.errors, удален')
