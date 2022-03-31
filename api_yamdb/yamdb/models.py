from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

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
        validators=[
            MinValueValidator(1800),
            MaxValueValidator(datetime.date.today().year),
        ],
        help_text='Год создания'
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
        help_text='Рейтинг'
    )
    description = models.CharField(
        max_length=400,
        null=True,
        blank=True,
        help_text='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        help_text='Жанр'
    )
    category = models.ManyToManyField(
        Category,
        through='CategoryTitle',
        related_name='titles',
        help_text='Категория'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name','year',],
                name='unique_title')
        ]

    def __str__(self):
        return self.name

class CategoryTitle(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'title',],
                name='unique_categorytitle')
        ]

    def __str__(self):
        return f'{self.title} {self.category}' 

class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title',],
                name='unique_genretitle')
        ]

    def __str__(self):
        return f'{self.title} {self.genre}' 