from django.db import transaction
from django.shortcuts import get_list_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response

from bucket.minio_client import delete_file

from utils.views import BaseViewSet
from utils.roles import PetRoles

from pet.models import Specie, Breed, Pet
from pet.serializers import SpecieSerializer, BreedSerializer, PetSerializer
from pet.filters import PetFilter, BreedFilter

from utils.exceptions import manage_exceptions
from utils.functions import has_permission, extract_file_photo_details
from utils.validations import validate_serializer_and_upload_file, image_validation


class SpecieViewSet(BaseViewSet): # não vai ser preciso personalizar, as regras de role são suficientes
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
    roles_required = PetRoles.SPECIE_ROLES

class BreedViewSet(BaseViewSet): # não vai ser preciso personalizar, as regras de role são suficientes
    filter_backends = [DjangoFilterBackend]
    filterset_class = BreedFilter
    
    queryset = Breed.objects.all() # Talvez adicionar um filtro de espécie para o list
    serializer_class = BreedSerializer
    roles_required = PetRoles.BREED_ROLES

    def list(self, request, *args, **kwargs):
        try:
            list_breeds = self.filter_queryset(self.get_queryset())
            list_serializer = self.serializer_class(list_breeds, many=True)
            return Response({'breeds': list_serializer.data}, status=status.HTTP_200_OK)
   
        except Exception as e:
            return manage_exceptions(e, context='list')    

class PetViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = PetFilter
    
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    roles_required = PetRoles.PET_ROLES

    folder_prefix = 'pets'

    def create(self, request):
        try:
            data = request.data

            if not has_permission(pk=data['pet_owner_id'], request=request, roles=self.roles_required['create']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            file = request.FILES.get('photo')
            file_name, content_type = None, None

            if file:
                image_validation(file=file)

                file_name, content_type = extract_file_photo_details(file)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
        
        except Exception as e:
            return manage_exceptions(e, context='create')

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                pet_id_photo = self.get_queryset().filter(pk=pk).values_list('pet_owner_id', flat=True).first() # so carrega o campo desejado

                if not has_permission(pk=str(pet_id_photo), request=request, roles=self.roles_required['destroy']):
                    return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

                if not pet_id_photo:
                    return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

                user_photo = self.get_queryset().get(pk=pk)  # recupera o objeto completo
                user_photo_path = user_photo.photo_path

                user_photo.delete()

                if user_photo.photo_path:
                    delete_success, e = delete_file(user_photo.photo_path)
                    if not delete_success:
                        raise Exception(e)

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

    def update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            data = request.data
            owner_id = self.get_queryset().filter(pk=pk).values_list('pet_owner_id', flat=True).first()
            print(owner_id)
            if not has_permission(pk=owner_id, request=request, roles=self.roles_required['create']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
            pet = self.get_queryset().get(pk=pk)
            file = request.FILES.get('photo')
            file_name, content_type = pet.photo_path.split('/')[-1] if pet.photo_path else None, None

            if file:
                image_validation(file=file)

                file_name, content_type = extract_file_photo_details(file, pet)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(pet, data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
            
        except Exception as e:
            return manage_exceptions(e, context='update')

    def partial_update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            data = request.data
            owner_id = self.get_queryset().filter(pk=pk).values_list('pet_owner_id', flat=True).first()

            if not has_permission(pk=owner_id, request=request, roles=self.roles_required['create']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
            pet = self.get_queryset().get(pk=pk)
            file = request.FILES.get('photo')
            file_name, content_type = pet.photo_path.split('/')[-1] if pet.photo_path else None, None

            if file:
                image_validation(file=file)

                file_name, content_type = extract_file_photo_details(file, pet)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(pet, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
            
        except Exception as e:
            return manage_exceptions(e, context='update')

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_retrive_total'] for role in request.roles):
                list_pets = self.filter_queryset(self.get_queryset()) # configurar os filtros depois
                list_serializer = self.serializer_class(list_pets, many=True)
                return Response({'pets': list_serializer.data}, status=status.HTTP_200_OK)
            # Posso criar um list_retrive_parcial, por exemplo para o médico ver apenas seus pacientes, vou pensar no caso
            # Vai ser interessante colocar, mas vou deixar pra quando as outras rotas tiverem completas
            # Está como uma tarefa a se fazer no todo do readme
            else:
                list_pets = get_list_or_404(self.get_queryset(), pet_owner_id=request.current_user_id)
                list_serializer = self.serializer_class(list_pets, many=True)
                return Response({'pets': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            owner_id = self.get_queryset().filter(pk=pk).values_list('pet_owner_id', flat=True).first() # so carrega o campo desejado

            if not has_permission(pk=str(owner_id), request=request, roles=self.roles_required['list_retrive_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not owner_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            pet = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            pet_serializer = self.serializer_class(pet)
            return Response({'usuário': pet_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
