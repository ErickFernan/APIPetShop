import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='iexact')
    price_min = django_filters.NumberFilter(field_name='sale_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='sale_price', lookup_expr='lte')
    product_type = django_filters.CharFilter(field_name='product_type', lookup_expr='iexact')
    expiration_date_min = django_filters.DateFilter(field_name='expiration_date', lookup_expr='gte')
    expiration_date_max = django_filters.DateFilter(field_name='expiration_date', lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_max = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')

    class Meta:
        model = Product
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.
