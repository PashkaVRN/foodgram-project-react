import json
from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = ' Загрузить данные в модель ингредиентов '

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Старт команды'))
        with open('data/ingredients.json', encoding='utf-8',
                  ) as data_file_ingredients:
            ingredient_data = json.loads(data_file_ingredients.read())
            for ingredients in ingredient_data:
                Ingredient.objects.get_or_create(**ingredients)

        with open('data/tags.json', encoding='utf-8',
                  ) as data_file_tags:
            tags_data = json.loads(data_file_tags.read())
            for tags in tags_data:
                Tag.objects.get_or_create(**tags)

        self.stdout.write(self.style.SUCCESS('Данные загружены'))
