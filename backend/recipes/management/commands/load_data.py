import json
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Upload data to Ingredients model'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Start command'))

        with open(
            os.path.abspath('data/ingredients.json')
        ) as data_file_ingredients:
            ingredient_data = json.loads(data_file_ingredients.read())
            for ingredients in ingredient_data:
                Ingredient.objects.get_or_create(**ingredients)

        self.stdout.write(self.style.SUCCESS('Data is uploaded'))
