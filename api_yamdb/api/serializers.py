from audioop import avg
from email.policy import default
from rest_framework import serializers, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator

from yamdb.models import (Category, Genre, Title, Review, Comment)


class CategorySerialaizer(serializers.ModelSerializer):
   # permission_classes = (IsModerator,)
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerialaizer(serializers.ModelSerializer):
   # permission_classes = (IsModerator,)
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
   # permission_classes = (IsModerator,)
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)
        read_only_fields = ('genre', 'category', 'category',)

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category',)
            )
        ]

    def get_rating(self, obj):
        if Review.objects.filter(
            title__name=obj.name,
            title__year=obj.year,
            title__category=obj.category
            ).count():
            title = get_object_or_404(
                Title,
                name=obj.name,
                year=obj.year,
                category=obj.category)
            rating = title.reviews.aggregate(rating=Avg('score'))
            return rating.get('rating')
        return 0

class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Title.objects.all()
    )

    class Meta:
        model = Review
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Title.objects.all()
    )
    review = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Review.objects.all()
    )

    class Meta:
        model = Comment
        fields = '__all__'
