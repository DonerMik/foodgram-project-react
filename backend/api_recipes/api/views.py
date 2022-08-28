from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientsRecipe, Recipes,
                            ShoppingCart, Subscribe, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filter import IngredientsFilter, RecipesFilter
from .paginator import CustomPagination
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipesSerializer,
                          RecipesShortSerializer, TagSerializer,
                          UserCustomSerializer, UsersSubscriptionsSerializer)

User = get_user_model()


def getting_user(self, request):
    user = request.user
    obj_user = User.objects.get(username=user)
    return obj_user


class UserCustomViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserCustomSerializer
    pagination_class = CustomPagination

    @action(detail=False)
    def subscriptions(self, request):
        obj_user = getting_user(self, request)
        serializer = UsersSubscriptionsSerializer(obj_user)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        obj_user = getting_user(self, request)
        sub_user = User.objects.get(id=id)
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


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend,]
    filterset_class = RecipesFilter
    permission_classes = [AuthorOrReadOnly]

    @action(detail=False, permission_classes=[IsAuthenticated],)
    def download_shopping_cart(self, request):
        ingredients = IngredientsRecipe.objects.filter(
            recipe__shopping_user__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_total=Sum('amount'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="ShoppingList.pdf"')
        pdf = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
        pdf.setTitle('Список покупок')
        pdf.setFont('Verdana', size=22)
        pdf.drawString(200, 770, 'Список покупок:')
        pdf.setFont('Verdana', size=16)
        height = 670
        for ing in ingredients:
            pdf.drawString(
                50,
                height,
                (
                    f"{ing['ingredient__name']} - "
                    f"{ing['ingredient_total']} "
                    f"{ing['ingredient__measurement_unit']}"
                )
            )
            height -= 25
        pdf.showPage()
        pdf.save()
        return response

    @action(detail=True, methods=['post', 'delete'],permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):

        obj_user = getting_user(self, request)
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        if request.method == "POST":
            ShoppingCart.objects.create(user=obj_user,
                                        recipes=recipe)

            return Response(serializer.data)
        ShoppingCart.objects.get(user=obj_user,
                                 recipes=recipe).delete()
        return Response('serializer.errors, удален')

    @action(detail=True, methods=['post', 'delete'],permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        obj_user = getting_user(self, request)
        recipe = Recipes.objects.get(pk=pk)
        serializer = RecipesShortSerializer(recipe)
        if request.method == "POST":
            Favorite.objects.create(user=obj_user,
                                        recipes=recipe)

            return Response(serializer.data)
        Favorite.objects.get(user=obj_user,
                                 recipes=recipe).delete()
        return Response('serializer.errors, удален')
