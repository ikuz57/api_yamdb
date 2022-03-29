from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Имя категории',
        help_text='Введите имя категории',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Уникальный идентификатор категории',
        help_text='Введите уникальный идентификатор категории',
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование жанра',
        help_text='Введите наименоване жанра',
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Уникальный идентификатор жанра',
        help_text='Введите уникальный идентификатор жанра'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4999),
        ],
        verbose_name='Год создания',
        help_text='Введите год создания произведения',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория',
        help_text='Введите категорию',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Выберите жанр',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание произведения'
    )

    def __str__(self):
        return self.name


class Revew(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='review',
        help_text='Выберите произведение',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Укажите автора',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка',
        help_text='Укажите вашу оценку произведения',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        help_text='Укажите дату отзыва',
    )

    class Meta:
        models.UniqueConstraint(fields=['author', 'title'],
                                name='unique_review')

    def __str__(self):
        return f'{self.title} - {self.author}'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Укажите автора',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение',
        help_text='Укажите произведение',
    )
    review = models.ForeignKey(
        Revew,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Укажите отзыв',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        help_text='Введите дату отзыва',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
