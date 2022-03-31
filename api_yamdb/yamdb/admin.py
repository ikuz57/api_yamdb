from django.contrib import admin
from yamdb.models import Category, Genre, Title, CategoryTitle, GenreTitle
# Register your models here.

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(CategoryTitle)
admin.site.register(GenreTitle)