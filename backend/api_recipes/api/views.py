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
    def create_or_delete_obj(self, request, user, obj2, cls, serializer):
        '''Метод создает объект с двумя полями.
        Первое из которых поле user'''
        if request.method == "POST":
            cls.objects.create(user, obj2)
            return Response(serializer.data)
        cls.objects.get(user, obj2).delete()
        return Response('serializer.errors, удален')

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
        user = request.user
        sub_user = User.objects.get_objects_or_404(id=id)
        serializer = UsersSubscriptionsSerializer(user)
        return self.create_or_delete_obj(request, user, sub_user,
                                         Subscribe,
                                         serializer)
        # if request.method == "POST":
        #     Subscribe.objects.create(user=obj_user,
        #                              author=sub_user)
        #     return Response(serializer.data)
        # Subscribe.objects.get(user=obj_user,
        #                       author=sub_user).delete()
        # return Response('serializer.errors, удален')


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
        user = request.user
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        return self.create_or_delete_obj(request, user, recipe,
                                         ShoppingCart,
                                         serializer)

        # if request.method == "POST":
        #     ShoppingCart.objects.create(user=obj_user,
        #                                 recipes=recipe)
        #
        #     return Response(serializer.data)
        # ShoppingCart.objects.get(user=obj_user,
        #                          recipes=recipe).delete()
        # return Response('serializer.errors, удален')

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user(self, request)
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        return self.create_or_delete_obj(request, user,
                                         recipe, Favorite,
                                         serializer)
        # if request.method == "POST":
        #     Favorite.objects.create(user=obj_user,
        #                             recipes=recipe)
        #
        #     return Response(serializer.data)
        # Favorite.objects.get(user=obj_user,
        #                          recipes=recipe).delete()
        # return Response('serializer.errors, удален')
