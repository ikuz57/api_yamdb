from audioop import avg
from email.policy import default
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

from yamdb.models import (Category, Genre, Title,
                          Review, Comment)

User = get_user_model()


class CategorySerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleCreateSerialaizer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        read_only_fields = ('genre', 'category',)

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category',)
            )
        ]


class TitleSerialaizer(serializers.ModelSerializer):
    genre = GenreSerialaizer(
        many=True,
        required=True,
    )
    category = CategorySerialaizer(required=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category',)

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
            return round(rating.get('rating'))
        return None


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        default='',
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', 'author',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                #message=('На одно произведение можно написать',
                #         'только один отзыв.'),
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all()
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Review.objects.all()
    )

    class Meta:
        model = Comment
        fields = '__all__'

