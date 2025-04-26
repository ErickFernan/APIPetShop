from utils.views import BaseViewSet
from utils.roles import HotelRoles
from utils.validations import validate_serializer_and_upload_file
from utils.exceptions import manage_exceptions
from utils.functions import has_permission, validate_required_fields

from hotel.models import Reservation, Service, ReservationService
from hotel.serializers import ReservationSerializer, ServiceSerializer, ReservationServiceSerializer, ReservationCreateSerializer
from hotel.filters import ServiceFilter, ReservationFilter

from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response


class ReservationViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    roles_required = HotelRoles.RESERVATION_ROLES

    def create(self, request):
        try:
            data = request.data.copy()
            data['seller_id'] = request.current_user_id

            extra_required_fields = ['pet_id']
            errors = validate_required_fields(data, extra_required_fields)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = ReservationCreateSerializer(data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
        
        except Exception as e:
            return manage_exceptions(e, context='create')
        

    def update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            reservation = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(reservation, data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')
        
    def partial_update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            reservation = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(reservation, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='partial_update')
        
    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_retrive_total'] for role in request.roles):
                list_reservations = self.filter_queryset(self.get_queryset())
                # list_reservations = self.get_queryset()  # Sem o filtro, retorna tudo
                list_serializer = self.serializer_class(list_reservations, many=True)
                return Response({'sale': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                list_reservations = get_list_or_404(self.get_queryset(), pet_id__pet_owner_id=request.current_user_id) # Esse caso vai ser chamado apenas se não for alguns dos usuários com acesso total, ou seja, se não for um superuser, estágiario ou atendente loja, dessa forma vai buscar pelo comprador(purchase)
                list_serializer = self.serializer_class(list_reservations, many=True)
                return Response({'sale': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                reservation = get_object_or_404(self.get_queryset(), id=pk)

                reservation.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

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
