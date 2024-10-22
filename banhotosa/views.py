from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from banhotosa.models import Appointment, ServiceType, ProductUsed
from banhotosa.serializers import AppointmentSerializer, ServiceTypeSerializer, ProductUsedSerializer

class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class ServiceTypeViewSet(ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

class ProductUsedViewSet(ModelViewSet):
    queryset = ProductUsed.objects.all()
    serializer_class = ProductUsedSerializer
