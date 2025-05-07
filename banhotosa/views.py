from utils.views import BaseViewSet
from utils.roles import BanhotosaRoles
from utils.validations import validate_serializer_and_upload_file
from utils.exceptions import manage_exceptions
from utils.functions import has_permission, validate_required_fields

from banhotosa.models import Appointment, ServiceType, ProductUsed, AppointmentService
from banhotosa.serializers import AppointmentSerializer, ServiceTypeSerializer, ProductUsedSerializer, AppointmentServiceSerializer, AppointmentCreateSerializer

from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import status
from rest_framework.response import Response

class AppointmentViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    roles_required = BanhotosaRoles.APPOINTMENT_ROLES

    def create(self, request): # preciso criar uma regra no save para verificar se conflitos de agenda.
        try:
            data = request.data.copy()
            data['func_id'] = request.current_user_id

            extra_required_fields = ['pet_id']
            errors = validate_required_fields(data, extra_required_fields)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = AppointmentCreateSerializer(data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
        
        except Exception as e:
            return manage_exceptions(e, context='create')
        
    def update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            appointment = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(appointment, data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')
        
    def partial_update(self, request, *args, **kwargs):  # Os metodos updates tb irão influenciar nos calculos de agendamento
        try:
            pk = kwargs.get('pk')
            appointment = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(appointment, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='partial_update')
        
    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_retrive_total'] for role in request.roles):
                # list_appointments = self.filter_queryset(self.get_queryset())
                list_appointments = self.get_queryset()  # Sem o filtro, retorna tudo
                list_serializer = self.serializer_class(list_appointments, many=True)
                return Response({'apointments': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                list_appointments = get_list_or_404(self.get_queryset(), pet_id__pet_owner_id=request.current_user_id) # Esse caso vai ser chamado apenas se não for alguns dos usuários com acesso total, ou seja, se não for um superuser, estágiario ou atendente loja, dessa forma vai buscar pelo comprador(purchase)
                list_serializer = self.serializer_class(list_appointments, many=True)
                return Response({'apointments': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            owner_id = self.get_queryset().filter(pk=pk).values_list('pet_id__pet_owner_id', flat=True).first() # so carrega o campo desejado

            if not has_permission(pk=str(owner_id), request=request, roles=self.roles_required['list_retrive_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            appoitment = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            appoitment_serializer = self.serializer_class(appoitment)
            return Response({'usuário': appoitment_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
        
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                appointment = get_object_or_404(self.get_queryset(), id=pk)

                appointment.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')
        

class ServiceTypeViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter

    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    roles_required = BanhotosaRoles.SERVICETYPE_ROLES

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
            service_type = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(service_type, data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')
        
    def partial_update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            service_type = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(service_type, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')

    def list(self, request, *args, **kwargs):
        try:
            # list_service_type = self.filter_queryset(self.get_queryset()) # preciso fazer o filtro para filtrar por nome tb
            list_service_type = self.get_queryset()  # Sem o filtro, retorna tudo
            list_serializer = self.serializer_class(list_service_type, many=True)
            return Response({'serviços': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            service_type = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            service_type_serializer = self.serializer_class(service_type)
            return Response({'serviço': service_type_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
        
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                service_type = get_object_or_404(self.get_queryset(), id=pk)

                service_type.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

class AppointmentServiceViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter   !!!!!!!!!!!!!! preço Preciso pegar automaticamente esse valor !!!!!!!!!!!!

    queryset = AppointmentService.objects.all()
    serializer_class = AppointmentServiceSerializer
    roles_required = BanhotosaRoles.APPOINTMENT_ROLES # mudar aqui para AppointmentServiceRoles quando criar a role

    def create(self, request):
        try:
            data = request.data
            serializer = AppointmentServiceSerializer(data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
        
        except Exception as e:
            return manage_exceptions(e, context='create')

class ProductUsedViewSet(BaseViewSet):
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ReservationServiceFilter

    queryset = ProductUsed.objects.all()
    serializer_class = ProductUsedSerializer
    roles_required = BanhotosaRoles.PRODUCTUSED_ROLES

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
            service_type = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(service_type, data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')
        
    def partial_update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            product_used = get_object_or_404(self.get_queryset(), id=pk)
            data = request.data

            serializer = self.serializer_class(product_used, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer=serializer)
            
        except Exception as e:
            return manage_exceptions(e, context='update')

    def list(self, request, *args, **kwargs):
        try:
            # list_product_used = self.filter_queryset(self.get_queryset()) # preciso fazer o filtro para filtrar por nome tb
            list_product_used = self.get_queryset()  # Sem o filtro, retorna tudo
            list_serializer = self.serializer_class(list_product_used, many=True)
            return Response({'produtos usados': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            product_used = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            product_used_serializer = self.serializer_class(product_used)
            return Response({'serviço': product_used_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
        
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                product_used = get_object_or_404(self.get_queryset(), id=pk)

                product_used.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')
