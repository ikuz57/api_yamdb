from audioop import avg
from email.policy import default
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from yamdb.models import Category, Genre, Review, Title
from django.db.models import Avg

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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        read_only_fields = ('genre', 'category',)

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year')
            )
        ]

    def get_rating(self, obj):
        if Review.objects.filter(
            title__name=obj.name,
            title__year=obj.year
            ).count():
            title = get_object_or_404(Title, name=obj.name, year=obj.year)
            rating = title.reviews.aggregate(rating=Avg('score'))
            return rating.get('rating')
        return 0