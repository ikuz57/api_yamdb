
# Generated by Django 2.2.16 on 2022-03-30 20:59


import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),

                ('name', models.CharField(help_text='Имя категории', max_length=200)),
                ('slug', models.SlugField(help_text='Уникальный идентификатор', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yamdb.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название жанра', max_length=200)),
                ('slug', models.SlugField(help_text='Уникальный идентификатор', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='yamdb.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название произведения', max_length=200)),
                ('year', models.IntegerField(help_text='Год создания', validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2022)])),
                ('rating', models.IntegerField(help_text='Рейтинг', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('description', models.CharField(blank=True, help_text='Описание', max_length=400, null=True)),
                ('category', models.ManyToManyField(help_text='Категория', related_name='titles', through='yamdb.CategoryTitle', to='yamdb.Category')),
                ('genre', models.ManyToManyField(help_text='Жанр', related_name='titles', through='yamdb.GenreTitle', to='yamdb.Genre')),
            ],
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yamdb.Title'),
        ),
        migrations.AddField(
            model_name='categorytitle',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='yamdb.Title'),
        ),
        migrations.AddConstraint(
            model_name='title',
            constraint=models.UniqueConstraint(fields=('name', 'year'), name='unique_title'),
        ),
        migrations.AddConstraint(
            model_name='genretitle',
            constraint=models.UniqueConstraint(fields=('genre', 'title'), name='unique_genretitle'),
        ),
        migrations.AddConstraint(
            model_name='categorytitle',
            constraint=models.UniqueConstraint(fields=('category', 'title'), name='unique_categorytitle'),
        ),
    ]
