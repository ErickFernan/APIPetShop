from keycloak_config.keycloak_client import (assign_role_to_user, set_password, get_role_info, 
                                            add_user_to_auth_service, delete_user_to_auth_service, get_user_info, 
                                            update_user_to_auth_service, rollback_update_keycloak, rollback_create_keycloak,
                                            get_user_info2, rollback_delete_keycloak)

from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404

from bucket.minio_client import delete_list_files, upload_file

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from utils.views import BaseViewSet
from utils.roles import UsuariosRoles
from utils.exceptions import manage_exceptions
from utils.validations import image_validation, audio_validation, validate_serializer_and_upload_file
from utils.functions import extract_file_details, has_permission

from usuarios.models import User, UserDocument, UserPhoto, UserAudio
from usuarios.serializers import (UserSerializer, UserCreateSerializer, UserDocumentSerializer, 
                                  UserPhotoSerializer, UserPhotoCreateSerializer, UserAudioSerializer, 
                                  UserAudioCreateSerializer)


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    roles_required = UsuariosRoles.USER_ROLES

    def create(self, request):
        """
        O  Create é público, ou seja, qualquer token pode criar um usuário, entretanto, um token
        ainda se faz necessário. Caso o token utilizado não seja o de um superuser a role e area
        é automáticamente modificado para 'user'. O que mantém um mínimo de segurança de acesso a rotas restritas
        mesmo com o create 'público'. Não é uma solução das mais robustas, mas cumpre seu papel neste projeto.
        """
        data = request.data.copy()

        # Verifica a role do token fornecido e já validado
        if not any(role in self.roles_required['create_total'] for role in request.roles):
            data['role'], data['area'] = 'user', 'user'

        serializer = UserCreateSerializer(data=data)
        
        try:
            if serializer.is_valid():

                password = serializer.validated_data.pop('password')
                
                with transaction.atomic():

                    user_auth_service_id = add_user_to_auth_service(username=data['username'], 
                                                                email=data['email'], 
                                                                firstName=data['first_name'], 
                                                                lastName=data['last_name'])

                    assign_role_to_user(user_auth_service_id, get_role_info(data['role']))
                    set_password(user_auth_service_id, password)
                    
                    serializer.validated_data['auth_service_id'] = user_auth_service_id
                    serializer.save()
                    user = get_object_or_404(self.queryset, email=data['email'])

                    update_user_to_auth_service(user_id=get_user_info(username=user.username),
                                                payload={"email": data.get('email', user.email),
                                                         "firstName": data.get('first_name', user.first_name),
                                                         "lastName": data.get('last_name', user.last_name),
                                                         "attributes": {
                                                            "django_uuid": [str(user.id)]
                                                        }})
                    
                    return Response({'message': 'Create successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
            return Response({'message': 'Create failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Rollback no keycloak em caso de falha
            if 'user_auth_service_id' in locals():
                rollback_create_keycloak(user_auth_service_id)
            
            return manage_exceptions(e, context='create')

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            
            if not has_permission(pk=pk, request=request, roles=self.roles_required['destroy_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            user = get_object_or_404(self.queryset, id=pk)
            user_id = user.id
            list_audios_path = [audio.audio_path for audio in UserAudio.objects.filter(user_id=pk)]
            list_photos_path = [photo.photo_path for photo in UserPhoto.objects.filter(user_id=pk)]
            
            with transaction.atomic():
                # Deletar usuário do keycloak
                user_auth_service_id = get_user_info(username=user.username) 
                delete_user_to_auth_service(user_auth_service_id)

                # Deletar usuário do Django
                user.delete()
                
                # Deletar fotos e audios relacionadas ao usuário
                delete_list_files(objects_name_list=list_photos_path + list_audios_path)
                  
            return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)       

        except Exception as e:
            if 'user_auth_service_id' in locals():
                response = rollback_delete_keycloak(user, user_id)
                if response:
                    return response
            return manage_exceptions(e, context='destroy')

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_total'] for role in request.roles):
                list_users = self.filter_queryset(self.queryset) # configurar os filtros depois
                list_serializer = self.serializer_class(list_users, many=True)
                return Response({'usuários': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                user = get_object_or_404(self.queryset, id=request.current_user_id)
                user_serializer = self.serializer_class(user)
                return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            
            if not has_permission(pk=pk, request=request, roles=self.roles_required['retrieve_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(self.queryset, id=pk)
            user_serializer = self.serializer_class(user)
            return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
    
    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            pk = kwargs.get('pk')

            if not has_permission(pk=pk, request=request, roles=self.roles_required['update_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(self.queryset, id=pk)

            if str(request.current_user_id) == pk:
                data['role'], data['area'] = user.role, user.area

            serializer = self.serializer_class(user, data=data, partial=True)
                
            if serializer.is_valid():
                # Atualizar no keycloak também
                user_auth_service_id = get_user_info(user.username)
                update_user_to_auth_service(user_id=user_auth_service_id,
                                            payload={"email": data.get('email', user.email),
                                                     "firstName": data.get('first_name', user.first_name),
                                                     "lastName": data.get('last_name', user.last_name)})
               
                serializer.save()

                return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_200_OK)
                
            return Response({'message': 'Update failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Rollback no keycloak em caso de falha
            if 'user_auth_service_id' in locals():
                rollback_update_keycloak(user_auth_service_id, user)      
            
            return manage_exceptions(e, context='partial_update')
    
    def update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            pk = kwargs.get('pk')

            if not has_permission(pk=pk, request=request, roles=self.roles_required['update_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(self.queryset, id=pk)

            if str(request.current_user_id) == str(user.auth_service_id):
                data['role'], data['area'] = user.role, user.area

            serializer = UserSerializer(user, data=data)
                
            if serializer.is_valid():
                # Atualizar no keycloak também
                user_auth_service_id = get_user_info(user.username)
                update_user_to_auth_service(user_id=user_auth_service_id,
                                            payload={"email": data.get('email', user.email),
                                                     "firstName": data.get('first_name', user.first_name),
                                                     "lastName": data.get('last_name', user.last_name)})
               
                serializer.save()

                return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_200_OK)
                
            return Response({'message': 'Update failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Rollback no keycloak em caso de falha
            if 'user_auth_service_id' in locals():
                rollback_update_keycloak(user_auth_service_id, user)  
            
            return manage_exceptions(e, context='update')
    
    
    @action(detail=True, methods=['put'])
    def update_password(self, request, *args, **kwargs): # colocar regra de permissão
        # Duvida para pesquisar depois: Esta função usa uma rota que o keycloak já disponibiliza normalemente. A questão é, neste caso eu devo aproveitar a API do keycloak
        # , ou seja, utilizar a própria rota do keycloak para fazer a troca da senha, ou eu devo criar esta rota na view igual eu fi aqui?
        # Esta dúvida se da principalmente pelo fato de eu querer usar o kong futuramente neste projeto, como ele é um gateway não teria necessidade de criar uma nova rota para tratar
        # esta função que diz respeito apenas ao keycloak, o kong centralizaria tudo. 
        # Quando for mecher na parte relacionada ao kong voltar aqui e analisar qual a melhor abordagem!!!!!!!
        try:
            password = request.data.get('password')
            if not password:
                return Response({"detail": "Password field is required."}, status=status.HTTP_400_BAD_REQUEST)

            pk = kwargs.get('pk')

            if not has_permission(pk=pk, request=request, roles=self.roles_required['update_password_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(self.queryset, id=pk)
            set_password(user.auth_service_id, password)
            
            return Response({'message': 'Update successful!'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='update_password')


class UserDocumentViewSet(BaseViewSet):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    roles_required = UsuariosRoles.USERDOCUMENT_ROLES


class UserPhotoViewSet(BaseViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = UserPhotoSerializer
    roles_required = UsuariosRoles.USERPHOTO_ROLES

    folder_prefix = 'usersphotos'

    def create(self, request):
        try:
            data = request.data.copy()

            if not has_permission(pk=data['user_id'], request=request, roles=self.roles_required['create_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            file = request.FILES.get('photo')
            file_name, content_type = None, None
        
            user = get_object_or_404(User, id=data['user_id'])

            if file:
                image_validation(file=file)

                file_name, content_type = extract_file_details(file)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = UserPhotoCreateSerializer(data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix, user)
        
        except Exception as e:
            return manage_exceptions(e, context='create')

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            
            if not has_permission(pk=pk, request=request, roles=self.roles_required['retrieve_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user_photo = get_object_or_404(self.queryset, id=pk)
            user_photo_serializer = self.serializer_class(user_photo)
            return Response({'usuário': user_photo_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_total'] for role in request.roles):
                list_user_photo = self.filter_queryset(self.queryset) # configurar os filtros depois
                list_serializer = self.serializer_class(list_user_photo, many=True)
                return Response({'usuários': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                print(request.current_user_id)
                list_user_photo = get_list_or_404(self.queryset, user_id=request.current_user_id)
                list_serializer = self.serializer_class(list_user_photo, many=True)
                return Response({'usuário': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')

    

  
class UserAudioViewSet(BaseViewSet):
    queryset = UserAudio.objects.all()
    serializer_class = UserAudioSerializer
    roles_required = UsuariosRoles.USERAUDIO_ROLES

    folder_prefix = 'usersaudios'

    def create(self, request):
        try:
            data = request.data

            if not has_permission(pk=data['user_id'], request=request, roles=self.roles_required['create_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            file = request.FILES.get('audio')
            file_name, content_type = None, None

            user = get_object_or_404(User, id=data['user_id'])

            if file:
                audio_validation(file=file)

                file_name, content_type = extract_file_details(file)
                data['audio_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = UserAudioCreateSerializer(data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix, user)
        
        except Exception as e:
            return manage_exceptions(e, context='create')
