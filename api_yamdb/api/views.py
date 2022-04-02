from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import CategorySerialaizer, GenreSerialaizer, TitleSerialaizer
from yamdb.models import Category, Genre, Title


class ListCreateDelete(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
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


