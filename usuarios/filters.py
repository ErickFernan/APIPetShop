import django_filters
from usuarios.models import User, UserAudio, UserDocument, UserPhoto

class UserFilter(django_filters.FilterSet):
    role = django_filters.CharFilter(field_name='role', lookup_expr='iexact')
    area = django_filters.CharFilter(field_name='area', lookup_expr='iexact')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='iexact')
    birthday_min = django_filters.DateFilter(field_name='birthday', lookup_expr='gte')
    birthday_max = django_filters.DateFilter(field_name='birthday', lookup_expr='lte')

    # Filtro personalizado para servidor de e-mail
    email_server = django_filters.CharFilter(method='filter_email_server')

    class Meta:
        model = User
        fields = []
        # fields = ['brand', 'product_type'] # Esse campo seria para criar filtros automaticos com o exact, o que não é o meu caso.

    
    def filter_email_server(self, queryset, name, value):
        """
        Filtra usuários pelo servidor de e-mail.
        Exemplo de entrada no filtro: "gmail" (para buscar emails @gmail.com).
        /api/users?email_server=gmail
        """
        return queryset.filter(email__icontains=f"@{value.lower()}")

class UserDocumentFilter(django_filters.FilterSet):
    doc_type = django_filters.CharFilter(field_name='doc_type', lookup_expr='iexact')
    
    class Meta:
        model = UserDocument
        fields = ['user_id']

class UserAudioFilter(django_filters.FilterSet):
    class Meta:
        model = UserAudio
        fields = ['user_id']

class UserPhotoFilter(django_filters.FilterSet):
    class Meta:
        model = UserPhoto
        fields = ['user_id']
        