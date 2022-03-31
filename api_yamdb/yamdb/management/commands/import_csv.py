from django.core.management.base import BaseCommand
import csv

from yamdb.models import Category, Comment, Genre, Review, Title, User

FILE_LIST = {
    #'api_yamdb\\static\\data\\category.csv': Category,
    #'api_yamdb\\static\\data\\genre.csv': Genre,
    'api_yamdb\\static\\data\\titles.csv': Title,
    # 'api_yamdb\\static\\data\\users.csv': User,
    # 'api_yamdb\\static\\data\\review.csv': Review,
    # 'api_yamdb\\static\\data\\comments.csv': Comment,
}


class Command(BaseCommand):
    help = 'Import data from csv files'

    def handle(self, *args, **options):
        for file_name, model in FILE_LIST.items():
            with open(file_name, 'r', newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile, quotechar='|')
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
            #try:
                print (line)
                model.objects.create(**line)
                created = created + 1
            #except Exception:
            #    print(f'Error while loading element {model}')
        return created
