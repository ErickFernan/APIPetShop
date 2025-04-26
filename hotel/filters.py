import django_filters

from hotel.models import Service

from utils.custom_filters import DateToEndOfDayFilter

class ServiceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='seller_id', lookup_expr='exact')
    price_per_day_min = django_filters.CharFilter(field_name='price_per_day', lookup_expr='gte')
    price_per_day_max = django_filters.CharFilter(field_name='price_per_day', lookup_expr='lte')

    class Meta:
        model = Service
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.
