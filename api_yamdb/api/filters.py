from django_filters import CharFilter, FilterSet
from yamdb.models import Title


class TitleFilterSet(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    
    class Meta:
        model = Title
        fields = ['category','genre','year','name']