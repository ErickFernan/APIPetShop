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

    # Filtro personalizado para buscar specie pelo nome
    breed_name = django_filters.CharFilter(method='filter_breed_name')
    pet_owner_name = django_filters.CharFilter(method='filter_pet_owner_name')

    class Meta:
        model = Pet
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    def filter_breed_name(self, queryset, name, value): # agora só copiar? conferir depois
        """
        Filtra as raças com base no nome da raça associada.
        """
        return queryset.filter(breed_id__name__iexact=value)

    def filter_pet_owner_name(self, queryset, name, value): # agora só copiar? conferir depois
        """
        Filtra as raças com base no nome do tutor associado.
        """
        return queryset.filter(pet_owner_id__first_name__iexact=value)


class BreedFilter(django_filters.FilterSet):
    specie_id = django_filters.CharFilter(field_name='specie_id', lookup_expr='exact')

    # Filtro personalizado para buscar specie pelo nome
    specie_name = django_filters.CharFilter(method='filter_specie_name')
    class Meta:
        model = Breed
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    def filter_specie_name(self, queryset, name, value): # agora só copiar? conferir depois
        """
        Filtra as raças com base no nome da espécie associada.
        """
        return queryset.filter(specie_id__name__iexact=value)
