from django.core.management.base import BaseCommand
import csv

from yamdb import models

FILE_LIST = {
    'api_yamdb\\static\\data\\category.csv': models.Category,
    'api_yamdb\\static\\data\\genre.csv': models.Genre,
    'api_yamdb\\static\\data\\titles.csv': models.Title,
    'api_yamdb\\static\\data\\genre_title.csv': models.GenreTitle,
    'api_yamdb\\static\\data\\users.csv': models.User,
    'api_yamdb\\static\\data\\review.csv': models.Review,
    'api_yamdb\\static\\data\\comments.csv': models.Comment,
}


class Command(BaseCommand):
    help = 'Import data from csv files'

    def handle(self, *args, **options):
        for file_name, model in FILE_LIST.items():
            with open(file_name, 'r', newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, quotechar='"')
                is_first_line = True
                lines = list()
                for row in reader:
                    if is_first_line:
                        head = row
                        is_first_line = False
                    else:
                        line = dict(zip(head, row))
                        lines.append(line)
                creted_num = self.CreateNewObject(model, lines)
                print(f'Created {creted_num} record, object {model}')

    def CreateNewObject(self, model, lines):
        created = 0
        for line in lines:
            print(line)
            model.objects.get_or_create(**line)
            created = created + 1
        return created
