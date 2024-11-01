from keycloak import KeycloakOpenIDConnection
from keycloak_config.keycloak_client import assign_role_to_user, set_password, get_role_info, add_user_to_auth_service, delete_user_to_auth_service, get_user_info, update_user_to_auth_service

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response

from utils.views import BaseViewSet
from utils.roles import UsuariosRoles

from usuarios.models import User, UserDocument, UserPhoto, UserAudio
from usuarios.serializers import UserSerializer, UserDocumentSerializer, UserPhotoSerializer, UserAudioSerializer


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

        serializer = self.serializer_class(data=data)
        try:
            if serializer.is_valid():

                password = serializer.validated_data.pop('password')
                
                with transaction.atomic():

                    user_auth_service_id = add_user_to_auth_service(username=data['email'], 
                                                                email=data['email'], 
                                                                firstName=data['first_name'], 
                                                                lastName=data['last_name'])

                    assign_role_to_user(user_auth_service_id, get_role_info(data['role']))
                    set_password(user_auth_service_id, password)
                    
                    serializer.validated_data['auth_service_id'] = user_auth_service_id
                    user = serializer.save()
                    
                    return Response({'message': 'Create successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
            return Response({'message': 'Create failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Rollback no keycloak em caso de falha
            if 'user_auth_service_id' in locals():
                try:
                    delete_user_to_auth_service(user_auth_service_id)
                except Exception as rollback_error:
                    return Response({'message': 'Falha no rollback do Keycloak', 'errors': str(rollback_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
            return Response({'message': 'Create failed!', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            user = get_object_or_404(self.queryset, id=pk)
            
            if any(role in self.roles_required['destroy_total'] for role in request.roles) or str(request.current_user_id) == str(user.auth_service_id):

                with transaction.atomic():

                    # Deletar usuário do keycloak
                    user_auth_service_id = get_user_info(email=user.email)
                    delete_user_to_auth_service(user_auth_service_id)

                    # Deletar usuário do Django
                    user.delete()

                    return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        except Http404:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": f"An unexpected error occurred22. {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_total'] for role in request.roles):
                list_users = self.filter_queryset(self.queryset)
                list_serializer = self.serializer_class(list_users, many=True)
                return Response({'usuários': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                user = get_object_or_404(self.queryset, auth_service_id=request.current_user_id)
                user_serializer = self.serializer_class(user)
                return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)
        
        except Http404:
            return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            user = get_object_or_404(self.queryset, id=pk)
            
            if not (any(role in self.roles_required['list_total'] for role in request.roles) or str(request.current_user_id) == str(user.auth_service_id)):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user_serializer = self.serializer_class(user)
            return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)

        except Http404:
            return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            pk = kwargs.get('pk')
            user = get_object_or_404(self.queryset, id=pk)

            if not (any(role in self.roles_required['list_total'] for role in request.roles) or str(request.current_user_id) == str(user.auth_service_id)):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            if str(request.current_user_id) == str(user.auth_service_id):
                data['role'], data['area'] = user.role, user.area

            serializer = self.serializer_class(user, data=data, partial=True)
                
            if serializer.is_valid():
                # Atualizar no keycloak também
                user_auth_service_id = get_user_info(user.email)
                update_user_to_auth_service(user_id=user_auth_service_id,
                                            payload={"email": data.get('email', user.email),
                                                     "firstName": data.get('first_name', user.first_name),
                                                     "lastName": data.get('last_name', user.last_name)})
               
                serializer.save()

                return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_200_OK)
                
            return Response({'message': 'Update failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Rollback no keycloak em caso de falha
            if 'user_auth_service_id' in locals():
                try:
                    update_user_to_auth_service(user_id=user_auth_service_id,
                                                payload={"email": user.email,
                                                         "firstName": user.first_name,
                                                         "lastName": user.last_name})
                except Exception as rollback_error:
                    return Response({'message': 'Falha no rollback do Keycloak', 'errors': str(rollback_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
            return Response({'message': 'Create failed!', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update_password():
        ...

class UserDocumentViewSet(BaseViewSet):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    roles_required = UsuariosRoles.USERDOCUMENT_ROLES


class UserPhotoViewSet(BaseViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = UserPhotoSerializer
    roles_required = UsuariosRoles.USERPHOTO_ROLES

    folder_prefix = 'usersphotos'


class UserAudioViewSet(BaseViewSet):
    queryset = UserAudio.objects.all()
    serializer_class = UserAudioSerializer
    roles_required = UsuariosRoles.USERAUDIO_ROLES

    folder_prefix = 'usersaudios'
