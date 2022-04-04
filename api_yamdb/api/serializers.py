from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title

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
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category',
        )

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
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message=('На одно произведение можно написать',
                         'только один отзыв.'),
            )
        ]

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (self.context['request'].parser_context['kwargs']
                        ['title_id'])
            author = self.context['request'].user
            review = Review.objects.filter(title_id=title_id, author=author)
            if review.exists():
                raise ValidationError(
                    detail=('К одному произведению можно оставить только '
                            + 'один отзыв.'),
                    code=status.HTTP_400_BAD_REQUEST,
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Title.objects.all(),
        default=None
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Review.objects.all(),
        default=None
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'
