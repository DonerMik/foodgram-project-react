import json
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Export data Ingredients and loading data into the database'

    def handle(self, *args, **kwargs):
        '''Функция загружает данные с json файла в базу данных Django'''
        file = '/home/donermik/foodgram-project-react/data/ingredients.json'
        with open(file, 'r') as f:
            contents = json.loads(f.read())

        count = 0
        for item in contents:
            name = item.get('name')
            measurement_unit = item.get('measurement_unit')

            Ingredient.objects.get_or_create(
                name=name,
                measurement_unit=measurement_unit
            )

            print('Ingridient создан')
            count += 1
            print(f'Объект № {count} загружен')

        print(f'Колличество загруженных элементов {count})')
        print('Ингридиенты загружены загружены')
