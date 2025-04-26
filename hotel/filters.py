import django_filters

from hotel.models import Service, Reservation, ReservationService

from utils.custom_filters import DateToEndOfDayFilter

class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='seller_id', lookup_expr='exact')
    price_per_day_min = django_filters.CharFilter(field_name='price_per_day', lookup_expr='gte')
    price_per_day_max = django_filters.CharFilter(field_name='price_per_day', lookup_expr='lte')

    class Meta:
        model = Service
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.


class ReservationFilter(django_filters.FilterSet):
    seller_id = django_filters.CharFilter(field_name='seller_id', lookup_expr='exact')
    pet_id = django_filters.CharFilter(field_name='pet_id', lookup_expr='exact')
    date_start_min = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    date_start_max = DateToEndOfDayFilter(field_name='start_date', lookup_expr='lte') # Esse mudança foi feita para garantir que o lte pegue todos os valores daquele dia
    date_end_min = django_filters.DateFilter(field_name='end_date', lookup_expr='gte')
    date_end_max = DateToEndOfDayFilter(field_name='end_date', lookup_expr='lte') # Esse mudança foi feita para garantir que o lte pegue todos os valores daquele dia
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    # Filtro personalizado para buscar pelos nomes e não pelo id
    seller_name = django_filters.CharFilter(method='filter_seller_name')
    pet_name = django_filters.CharFilter(method='filter_pet_name')
    pet_owner_first_name = django_filters.CharFilter(method='filter_pet_owner_first_name')


    class Meta:
        model = Reservation
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    def filter_seller_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do vendedor.
        """
        return queryset.filter(seller_id__first_name__iexact=value)

    def filter_pet_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do comprador.
        """
        return queryset.filter(pet_id__name__iexact=value)

    def filter_pet_owner_first_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do comprador.
        """
        return queryset.filter(pet_id__pet_owner_id__first_name__iexact=value)
    

class ReservationServiceFilter(django_filters.FilterSet):
    reservation_id = django_filters.CharFilter(field_name='reservation_id', lookup_expr='exact')
    service_id = django_filters.CharFilter(field_name='service_id', lookup_expr='exact')

    class Meta:
        model = ReservationService
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    # Filtro personalizado para buscar pelos nomes e não pelo id
    service_name = django_filters.CharFilter(method='filter_service_name')
    pet_name = django_filters.CharFilter(method='filter_pet_name')
    pet_owner_first_name = django_filters.CharFilter(method='filter_pet_owner_first_name')

    def filter_service_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do vendedor.
        """
        return queryset.filter(service_id__name__iexact=value)

    def filter_pet_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do comprador.
        """
        return queryset.filter(reservation_id__pet_id__name__iexact=value)
    
    def filter_pet_owner_first_name(self, queryset, name, value):
        """
        Filtra pelo nome próprio do comprador.
        """
        return queryset.filter(reservation_id__pet_id__pet_owner_id__first_name__iexact=value)
    