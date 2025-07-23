import django_filters

from banhotosa.models import Appointment, ServiceType, ProductUsed, AppointmentService


class AppointmentFilter(django_filters.FilterSet):
    pet_id = django_filters.CharFilter(field_name='pet_id', lookup_expr='exact')
    func_id = django_filters.CharFilter(field_name='func_id', lookup_expr='exact')
    date_min = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_max = django_filters.DateFilter(field_name='date', lookup_expr='lte')
                                                                                              # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    pet_name2 = django_filters.CharFilter(field_name='pet_id__name', lookup_expr='icontains') # Para lógicas mais simples na consulta posso fazer desse jeito.
                                                                                              # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
    # Filtro personalizado para buscar pelo nome
    pet_name = django_filters.CharFilter(method='filter_pet_name')
    func_name = django_filters.CharFilter(method='filter_func_name')


    class Meta:
        model = Appointment
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    def filter_pet_name(self, queryset, name, value): 
        """
        Filtra as raças com base no nome do pet.
        """
        return queryset.filter(pet_id__name__iexact=value)
    
    def filter_func_name(self, queryset, name, value): 
        """
        Filtra as raças com base no nome do funcionario.
        """
        return queryset.filter(func_id__first_name__iexact=value)

class ServiceTypeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    base_price_min = django_filters.NumberFilter(field_name='base_price', lookup_expr='gte')
    base_price_max = django_filters.NumberFilter(field_name='base_price', lookup_expr='lte')
    execution_time_min = django_filters.TimeFilter(field_name='execution_time', lookup_expr='gte')
    execution_time_max = django_filters.TimeFilter(field_name='execution_time', lookup_expr='lte')

    class Meta:
        model = ServiceType
        fields = []


class ProductUsedFilter(django_filters.FilterSet):
    product_id = django_filters.CharFilter(field_name='product_id', lookup_expr='exact')
    product_name = django_filters.CharFilter(field_name='product_id__name', lookup_expr='icontains')
    service_type_id = django_filters.CharFilter(field_name='service_type_id', lookup_expr='exact')
    service_type_name = django_filters.CharFilter(field_name='service_type_id__name', lookup_expr='icontains')

    class Meta:
        model = ProductUsed
        fields = []


class AppointmentServiceFilter(django_filters.FilterSet):
    appointment_id = django_filters.NumberFilter(field_name='appointment_id', lookup_expr='exact')
    service_type_id = django_filters.NumberFilter(field_name='service_type_id', lookup_expr='exact')
    service_type_name = django_filters.CharFilter(field_name='service_type_id__name', lookup_expr='icontains')
    charged_price_min = django_filters.DateFilter(field_name='charged_price', lookup_expr='gte')
    charged_price_max = django_filters.DateFilter(field_name='charged_price', lookup_expr='lte')
      

    class Meta:
        model = AppointmentService
        fields = []
