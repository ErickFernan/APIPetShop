import django_filters
from pet.models import Pet, Breed

class PetFilter(django_filters.FilterSet):
    pet_owner_id = django_filters.CharFilter(field_name='pet_owner_id', lookup_expr='exact')
    breed_id = django_filters.CharFilter(field_name='breed_id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    weight_min = django_filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = django_filters.NumberFilter(field_name='weight', lookup_expr='lte')
    birthday_min = django_filters.DateFilter(field_name='birthday', lookup_expr='gte')
    birthday_max = django_filters.DateFilter(field_name='birthday', lookup_expr='lte')

    class Meta:
        model = Pet
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

class BreedFilter(django_filters.FilterSet):
    specie_id = django_filters.CharFilter(field_name='specie_id', lookup_expr='exact')

    class Meta:
        model = Breed
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.
