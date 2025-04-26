from utils.views import BaseViewSet
from utils.roles import HotelRoles
from utils.validations import validate_serializer_and_upload_file
from utils.exceptions import manage_exceptions

from hotel.models import Reservation, Service, ReservationService
from hotel.serializers import ReservationSerializer, ServiceSerializer, ReservationServiceSerializer
from hotel.filters import ServiceFilter

from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response


class ReservationViewSet(BaseViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    roles_required = HotelRoles.RESERVATION_ROLES

class ServiceViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    roles_required = HotelRoles.SERVICE_ROLES

    def create(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
        
        except Exception as e:
            return manage_exceptions(e, context='create')
        
    def update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            service = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(service, data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')
        
    def partial_update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            service = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(service, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')

    def list(self, request, *args, **kwargs):
        """
        No list de produtos eu fiz um serializer que demilitava os campos a serem retornados, alguns não faziam sentido em retornar para o usuário comum,
        mas nesse caso não vi necessidade de fazer o mesmo.
        """
        try:
            list_service = self.filter_queryset(self.get_queryset()) # preciso fazer o filtro para filtrar por nome tb
            # list_service = self.get_queryset()  # Sem o filtro, retorna tudo
            list_serializer = self.serializer_class(list_service, many=True)
            return Response({'serviços': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            service = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            service_serializer = self.serializer_class(service)
            return Response({'serviço': service_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
        
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                service = get_object_or_404(self.get_queryset(), id=pk)

                service.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

class ReservationServiceViewSet(BaseViewSet):
    queryset = ReservationService.objects.all()
    serializer_class = ReservationServiceSerializer
    roles_required = HotelRoles.RESERVATIONSERVICE_ROLES
