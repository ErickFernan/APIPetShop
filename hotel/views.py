from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from hotel.models import Reservation, Service, ReservationService
from hotel.serializers import ReservationSerializer, ServiceSerializer, ReservationServiceSerializer
class ReservationViewSet(ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ReservationServiceViewSet(ModelViewSet):
    queryset = ReservationService.objects.all()
    serializer_class = ReservationServiceSerializer
