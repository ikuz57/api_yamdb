from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Имя категории',
    )
    slug = models.SlugField(
        unique=True,
        help_text='Уникальный идентификатор'
    )

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        help_text='Уникальный идентификатор'
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
    rating = models.IntegerField(
        help_text='Рейтинг'
    )
    description = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        help_text='Описание'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        help_text='Категория'
    )

    def __str__(self):
        return self.name