from django.contrib.admin import ModelAdmin, site

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CommentAdmin(ModelAdmin):
    list_display = ('id', 'author', 'title', 'review', 'pub_date', 'text')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')


class GenreAdmin(ModelAdmin):
    list_display = ('id', 'name', 'slug')


class ReviewAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author', 'text', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('author', 'pub_date')


class TitleAdmin(ModelAdmin):
    list_display = ('id', 'name', 'year', 'description')
    # search_fields = ('description',)
    # list_filter = ('genre', 'year')


site.register(Category, CategoryAdmin)
site.register(Comment, CommentAdmin)
site.register(Genre, GenreAdmin)
site.register(Review, ReviewAdmin)
site.register(Title, TitleAdmin)
