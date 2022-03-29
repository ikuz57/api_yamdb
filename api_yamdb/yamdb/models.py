from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Имя категории',
    )
    slug = models.SlugField(
        unique=True,
        help_text='Уникальный идентификатор категории'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Название произведения',
    )
    year = models.IntegerField(
        help_text='Год создания'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='Категория',
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    pass


class Revew(models.Model):
    pass


class Comment(models.Model):
    pass
