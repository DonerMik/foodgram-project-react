from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import IngredientsRecipe


def get_pdf(request):
    ''' Создает PDF файл со списком покупок'''

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
