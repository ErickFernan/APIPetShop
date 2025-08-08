from utils.views import BaseViewSet
from utils.roles import SaudeRoles
from utils.exceptions import manage_exceptions
from utils.validations import validate_serializer_and_upload_file, pdf_image_validation, image_validation
from utils.functions import has_permission, validate_required_fields, extract_file_photo_details, extract_file_photo_pdf_details

from saude.models import TreatmentCycle, Service, ExamType, Exam
from saude.serializers import TreatmentCycleSerializer, ServiceSerializer, ExamTypeSerializer, ExamSerializer, TreatmentCycleCreateSerializer, ServiceCreateSerializer, ExamCreateSerializer
from saude.filters import TreatmentCycleFilter, ServiceFilter, ExamTypeFilter, ExamFilter


from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response

from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404

from bucket.minio_client import delete_file


class TreatmentCycleViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = TreatmentCycleFilter

    queryset = TreatmentCycle.objects.all()
    serializer_class = TreatmentCycleSerializer
    roles_required = SaudeRoles.TREATMENTCYCLE_ROLES

    def create(self, request):
        try:
            data = request.data.copy()

            extra_required_fields = ['pet_id']
            errors = validate_required_fields(data, extra_required_fields)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TreatmentCycleCreateSerializer(data=data)

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
                list_cicles = self.filter_queryset(self.get_queryset())
                # list_cicles = self.get_queryset()  # Sem o filtro, retorna tudo
                list_serializer = self.serializer_class(list_cicles, many=True)
                return Response({'TreatmenCycles': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                list_cicles = get_list_or_404(self.get_queryset(), pet_id__pet_owner_id=request.current_user_id) # Esse caso vai ser chamado apenas se não for alguns dos usuários com acesso total, ou seja, se não for um superuser, estágiario ou atendente loja, dessa forma vai buscar pelo comprador(purchase)
                list_serializer = self.serializer_class(list_cicles, many=True)
                return Response({'TreatmenCycles': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            pet_owner_id = self.get_queryset().filter(pk=pk).values_list('pet_id__pet_owner_id', flat=True).first() # so carrega o campo desejado

            if not has_permission(pk=str(pet_owner_id), request=request, roles=self.roles_required['list_retrive_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not pet_owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            treatmentcycle = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            treatmentcycle_serializer = self.serializer_class(treatmentcycle)
            return Response({'treatmentcycle': treatmentcycle_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
        
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
    roles_required = SaudeRoles.SERVICE_ROLES

    def create(self, request): # PRECISO DE ALGO PARA LIMITAR QUEM PODE SER DESIGNADO COMO RESPONSÁVEL NA CRIAÇÃO?
        try:
            data = request.data.copy()

            extra_required_fields = ['responsible_id', 'start_date', 'cycle_id']
            errors = validate_required_fields(data, extra_required_fields)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
            serializer = ServiceCreateSerializer(data=data)

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
                list_services = self.filter_queryset(self.get_queryset())
                # list_services = self.get_queryset()  # Sem o filtro, retorna tudo
                list_serializer = self.serializer_class(list_services, many=True)
                return Response({'Services': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                list_services = get_list_or_404(self.get_queryset(), cycle_id__pet_id__pet_owner_id=request.current_user_id) # Esse caso vai ser chamado apenas se não for alguns dos usuários com acesso total, ou seja, se não for um superuser, estágiario ou atendente loja, dessa forma vai buscar pelo comprador(purchase)
                list_serializer = self.serializer_class(list_services, many=True)
                return Response({'Services': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            pet_owner_id = self.get_queryset().filter(pk=pk).values_list('cycle_id__pet_id__pet_owner_id', flat=True).first() # so carrega o campo desejado

            if not has_permission(pk=str(pet_owner_id), request=request, roles=self.roles_required['list_retrive_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not pet_owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            service = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            service_serializer = self.serializer_class(service)
            return Response({'service': service_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
        
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                reservation = get_object_or_404(self.get_queryset(), id=pk)

                reservation.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

class ExamTypeViewSet(BaseViewSet): # não vai ser preciso personalizar, as regras de role são suficientes
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExamTypeFilter
    
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    roles_required = SaudeRoles.EXAMTYPE_ROLES

class ExamViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExamFilter

    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    roles_required = SaudeRoles.EXAM_ROLES

    folder_prefix = 'exams'

    def create(self, request):
        try:
            data = request.data.copy()

            extra_required_fields = ['exam_type_id', 'service_id']
            errors = validate_required_fields(data, extra_required_fields)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            # if not has_permission(pk=data['pet_owner_id'], request=request, roles=self.roles_required['create']):
            #     return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            file = request.FILES.get('file')
            file_name, content_type = None, None

            if file:
                # image_validation(file=file) # Criar o pdf validation, e talvez uma opção para escolher entre imagem e pdf
                pdf_image_validation(file = file)

                file_name, content_type = extract_file_photo_details(file)
                data['result_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = ExamCreateSerializer(data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
        
        except Exception as e:
            return manage_exceptions(e, context='create')

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
   
                exam_file = self.get_queryset().get(pk=pk)  # recupera o objeto completo
                exam_file_path = exam_file.result_path

                exam_file.delete()

                if exam_file.result_path:
                    delete_success, e = delete_file(exam_file.result_path)
                    if not delete_success:
                        raise Exception(e)

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

    def update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            data = request.data.copy()

            exam = self.get_queryset().get(pk=pk)
            file = request.FILES.get('file')
            file_name, content_type = exam.result_path.split('/')[-1] if exam.result_path else None, None

            if file:
                # image_validation(file=file)
                pdf_image_validation(file=file)

                file_name, content_type = extract_file_photo_pdf_details(file, exam)
                data['result_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(exam, data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
            
        except Exception as e:
            return manage_exceptions(e, context='update')

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Partial Update not allowed for Exam.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_retrive_total'] for role in request.roles):
                list_exams = self.filter_queryset(self.get_queryset())
                # list_exams = self.get_queryset()  # Sem o filtro, retorna tudo
                list_serializer = self.serializer_class(list_exams, many=True)
                return Response({'Exams': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                list_exams = get_list_or_404(self.get_queryset(), service_id__cycle_id__pet_id__pet_owner_id=request.current_user_id) # Esse caso vai ser chamado apenas se não for alguns dos usuários com acesso total, ou seja, se não for um superuser, estágiario ou atendente loja, dessa forma vai buscar pelo comprador(purchase)
                list_serializer = self.serializer_class(list_exams, many=True)
                return Response({'Exams': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            pet_owner_id = self.get_queryset().filter(pk=pk).values_list('service_id__cycle_id__pet_id__pet_owner_id', flat=True).first() # so carrega o campo desejado

            if not has_permission(pk=str(pet_owner_id), request=request, roles=self.roles_required['list_retrive_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not pet_owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            exam = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            exam_serializer = self.serializer_class(exam)
            return Response({'Exam': exam_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
