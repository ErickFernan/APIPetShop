from utils.views import BaseViewSet
from utils.roles import PRODUCTS_ROLES

from hotel.models import Reservation, Service, ReservationService
from hotel.serializers import ReservationSerializer, ServiceSerializer, ReservationServiceSerializer


class ReservationViewSet(BaseViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    roles_required = PRODUCTS_ROLES

class ServiceViewSet(BaseViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    roles_required = PRODUCTS_ROLES

class ReservationServiceViewSet(BaseViewSet):
    queryset = ReservationService.objects.all()
    serializer_class = ReservationServiceSerializer
    roles_required = PRODUCTS_ROLES
