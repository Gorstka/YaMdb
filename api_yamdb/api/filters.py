from django_filters import ModelMultipleChoiceFilter, FilterSet, CharFilter

from reviews.models import Title, Genre, Category


class ModelFilter(FilterSet):
    genre = ModelMultipleChoiceFilter(
        field_name='genre__slug',
        queryset=Genre.objects.all(),
        to_field_name='slug')
    category = ModelMultipleChoiceFilter(
        field_name='category__slug',
        queryset=Category.objects.all(),
        to_field_name='slug')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = ModelMultipleChoiceFilter(
        field_name='year',
        queryset=Title.objects.all(),
        to_field_name='year')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'name', 'year')
