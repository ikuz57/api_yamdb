from unicodedata import category
from rest_framework import serializers
from yamdb.models import Category, Genre, Title

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
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'