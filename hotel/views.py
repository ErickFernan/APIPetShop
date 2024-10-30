from utils.views import BaseViewSet
from utils.roles import HotelRoles

from hotel.models import Reservation, Service, ReservationService
from hotel.serializers import ReservationSerializer, ServiceSerializer, ReservationServiceSerializer


class ReservationViewSet(BaseViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    roles_required = HotelRoles.RESERVATION_ROLES

class ServiceViewSet(BaseViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    roles_required = HotelRoles.SERVICE_ROLES

class ReservationServiceViewSet(BaseViewSet):
    queryset = ReservationService.objects.all()
    serializer_class = ReservationServiceSerializer
    roles_required = HotelRoles.RESERVATIONSERVICE_ROLES
