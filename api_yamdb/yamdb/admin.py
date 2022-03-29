from django.contrib import admin

from .models import Category, Comment, Genre, Revew, Title


class CategoryAdmin (admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


admin.site.register(Category, CategoryAdmin)
