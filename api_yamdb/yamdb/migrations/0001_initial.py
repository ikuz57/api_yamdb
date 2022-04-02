# Generated by Django 2.2.16 on 2022-04-02 17:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя категории', max_length=200)),
                ('slug', models.SlugField(help_text='Введите уникальный идентификатор категории', unique=True, verbose_name='Уникальный идентификатор категории')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименоване жанра', max_length=200, verbose_name='Наименование жанра')),
                ('slug', models.SlugField(help_text='Введите уникальный идентификатор жанра', unique=True, verbose_name='Уникальный идентификатор жанра')),
            ],
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yamdb.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения', max_length=200, verbose_name='Название произведения')),
                ('year', models.IntegerField(help_text='Введите год создания произведения', validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2022)], verbose_name='Год создания')),
                ('description', models.CharField(blank=True, help_text='Описание', max_length=400, null=True)),
                ('category', models.ForeignKey(blank=True, help_text='Категория', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='yamdb.Category')),
                ('genre', models.ManyToManyField(help_text='Жанр', related_name='titles', through='yamdb.GenreTitle', to='yamdb.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Введите текст отзыва', verbose_name='Текст отзыва')),
                ('score', models.IntegerField(help_text='Укажите вашу оценку произведения', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Укажите дату отзыва', verbose_name='Дата отзыва')),
                ('author', models.ForeignKey(help_text='Укажите автора', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('title', models.ForeignKey(help_text='Выберите произведение', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='yamdb.Title', verbose_name='review')),
            ],
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yamdb.Title'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Введите дату отзыва', verbose_name='Дата отзыва')),
                ('text', models.TextField(help_text='Введите текст отзыва', verbose_name='Текст отзыва')),
                ('author', models.ForeignKey(help_text='Укажите автора', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('review', models.ForeignKey(help_text='Укажите отзыв', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='yamdb.Review', verbose_name='Отзыв')),
                ('title', models.ForeignKey(help_text='Укажите произведение', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='yamdb.Title', verbose_name='Произведение')),
            ],
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.UniqueConstraint(fields=('name', 'year', 'category'), name='unique_title'),
        ),
        migrations.AddConstraint(
            model_name='genretitle',
            constraint=models.UniqueConstraint(fields=('genre', 'title'), name='unique_genretitle'),
        ),
    ]
