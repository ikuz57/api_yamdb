from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from yamdb.models import Category, Genre, Title, CategoryTitle, GenreTitle

class CategorySerialaizer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('name', 'slug',)

class GenreSerialaizer(serializers.ModelSerializer):

    class Meta: 
        model = Genre
        fields = ('name', 'slug',)

class TitleSerialaizer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Category.objects.all(),
        required=True
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('genre', 'category',)

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]
