from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilters(FilterSet):
    """Фильтрация по полям модели Title."""
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    name = CharFilter(lookup_expr='icontains')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = '__all__'
