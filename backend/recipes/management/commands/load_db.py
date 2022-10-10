import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    '''This is a class for import data from csv file to database.'''

    def handle(self, *args, **options):
        with open(
            'recipes/management/commands/data/ingredients.csv', 'r'
        ) as file:
            data = csv.reader(file, delimiter=',')
            for row in data:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
