from utils.views import BaseViewSet
from utils.roles import BanhotosaRoles

from banhotosa.models import Appointment, ServiceType, ProductUsed
from banhotosa.serializers import AppointmentSerializer, ServiceTypeSerializer, ProductUsedSerializer

class AppointmentViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    roles_required = BanhotosaRoles.APPOINTMENT_ROLES

class ServiceTypeViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter

    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    roles_required = BanhotosaRoles.SERVICETYPE_ROLES

class ProductUsedViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter

    queryset = ProductUsed.objects.all()
    serializer_class = ProductUsedSerializer
    roles_required = BanhotosaRoles.PRODUCTUSED_ROLES
