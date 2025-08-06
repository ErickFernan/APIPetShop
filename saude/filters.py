import django_filters

from saude.models import TreatmentCycle, Service, ExamType, Exam

from utils.custom_filters import DateToEndOfDayFilter


class TreatmentCycleFilter(django_filters.FilterSet):
    pet_id = django_filters.CharFilter(field_name='pet_id', lookup_expr='exact')
    pet_name = django_filters.CharFilter(field_name='pet_id__name', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    start_date_min = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_max = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')

    class Meta:
        model = TreatmentCycle
        fields = []

class ServiceFilter(django_filters.FilterSet):
    responsible_id = django_filters.CharFilter(field_name='responsible_id', lookup_expr='exact')
    responsible_name = django_filters.CharFilter(field_name='responsible_id__first_name', lookup_expr='icontains')
    assistant_id = django_filters.CharFilter(field_name='assistant_id', lookup_expr='exact')
    assistant_name = django_filters.CharFilter(field_name='assistant_id__first_name', lookup_expr='icontains')
    service_type = django_filters.CharFilter(field_name='service_type', lookup_expr='icontains')
    start_date_min = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_max = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')
    return_date_min = django_filters.DateFilter(field_name='return_date', lookup_expr='gte')
    return_date_max = django_filters.DateFilter(field_name='return_date', lookup_expr='lte')
    cycle_id = django_filters.CharFilter(field_name='cycle_id', lookup_expr='exact')

    class Meta:
        model = Service
        fields = []

class ExamTypeFilter(django_filters.FilterSet):
    exam_name = django_filters.CharFilter(field_name='name', lookup_expr='icontains') # Este filtro é pra procurar nomes parecidos, tipo raiox torax e raiox braço, se buscar por raiox

    class Meta:
        model = ExamType
        fields = []

class ExamFilter(django_filters.FilterSet):
    exam_type_id = django_filters.CharFilter(field_name='exam_type_id', lookup_expr='exact')
    exam_type_name = django_filters.CharFilter(field_name='exam_type_id__name', lookup_expr='icontains')
    service_id = django_filters.CharFilter(field_name='service_id', lookup_expr='exact')
    service_type_name = django_filters.CharFilter(field_name='service_id__service_type', lookup_expr='icontains')
    pet_name = django_filters.CharFilter(field_name='service_id__cycle_id__pet_id__name', lookup_expr='icontains')
    assistant_name = django_filters.CharFilter(field_name='service_id__assistant_id__first_name', lookup_expr='icontains')
    responsible_name = django_filters.CharFilter(field_name='service_id__responsible_id__first_name', lookup_expr='icontains')
    pet_id = django_filters.CharFilter(field_name='service_id__cycle_id__pet_id', lookup_expr='exact')
    assistant_id = django_filters.CharFilter(field_name='service_id__assistant_id', lookup_expr='exact')    
    responsible_id = django_filters.CharFilter(field_name='service_id__responsible_id', lookup_expr='exact')
    start_date_min = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    start_date_max = DateToEndOfDayFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Exam
        fields = []
