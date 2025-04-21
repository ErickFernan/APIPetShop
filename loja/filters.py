import django_filters

from loja.models import Sale

from utils.custom_filters import DateToEndOfDayFilter

class SaleFilter(django_filters.FilterSet):
    seller_id = django_filters.CharFilter(field_name='seller_id', lookup_expr='exact')
    purchase_id = django_filters.CharFilter(field_name='purchase_id', lookup_expr='exact')
    date_min = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_max = DateToEndOfDayFilter(field_name='created_at', lookup_expr='lte') # Esse mudança foi feita para garantir que o lte pegue todos os valores daquele dia

    # Filtro personalizado para buscar pelos nomes e não pelo id
    seller_name = django_filters.CharFilter(method='filter_seller_name')
    purchase_name = django_filters.CharFilter(method='filter_purchase_name')

    class Meta:
        model = Sale
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    def filter_seller_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do vendedor.
        """
        return queryset.filter(seller_id__name__iexact=value)

    def filter_purchase_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do comprador.
        """
        return queryset.filter(purchase_id__first_name__iexact=value)


# class BreedFilter(django_filters.FilterSet):
#     specie_id = django_filters.CharFilter(field_name='specie_id', lookup_expr='exact')

#     # Filtro personalizado para buscar specie pelo nome
#     specie_name = django_filters.CharFilter(method='filter_specie_name')
#     class Meta:
#         model = Breed
#         fields = []
#         # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

#     def filter_specie_name(self, queryset, name, value): # agora só copiar? conferir depois
#         """
#         Filtra as raças com base no nome da espécie associada.
#         """
#         return queryset.filter(specie_id__name__iexact=value)
