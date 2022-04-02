from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, permissions

from .serializers import (CategorySerialaizer, GenreSerialaizer,
                          TitleSerialaizer, ReviewSerializer,
                          CommentSerializer)

from yamdb.models import Category, Genre, Title, Review, Comment
from users.permissions import IsAuthorOrReadOnly, IsModerator, IsSuperuser


class ListCreateDelete(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                       mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class PatchDelete(mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    pass


class CategoriesViewSet(ListCreateDelete):
    queryset = Category.objects.all()
    serializer_class = CategorySerialaizer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=slug',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateDelete):
    queryset = Genre.objects.all()
    serializer_class = GenreSerialaizer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=slug',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerialaizer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthorOrReadOnly, IsModerator, IsSuperuser)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = get_object_or_404(Title, pk=title_id).reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAuthorOrReadOnly, IsModerator, IsSuperuser)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        new_queryset = get_object_or_404(Review, pk=review_id).comments.all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
