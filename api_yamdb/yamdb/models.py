from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Имя категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор категории',
        help_text='Введите уникальный идентификатор категории',
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование жанра',
        help_text='Введите наименоване жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор жанра',
        help_text='Введите уникальный идентификатор жанра'
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Название произведения',
        verbose_name='Название произведения',
    )

    year = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.date.today().year),
        ],
        verbose_name='Год создания',
        help_text='Введите год создания произведения',
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        help_text='Категория'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category', ],
                name='unique_title')
        ]

    def __str__(self):
        return self.name


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
                fields=['genre', 'title', ],
                name='unique_genretitle')
        ]

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Укажите автора',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='review',
        help_text='Выберите произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва',
        blank=False,
        null=False,
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name='Оценка',
        help_text='Укажите вашу оценку произведения',
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        help_text='Укажите дату отзыва',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            )
        ]

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
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Укажите отзыв',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Произведение',
        help_text='Укажите произведение',
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

    def save(self, *args, **kwargs):
        self.title = self.review.title
        super().save(*args, **kwargs)
