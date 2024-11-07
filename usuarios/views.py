from keycloak import KeycloakOpenIDConnection
from keycloak_config.keycloak_client import assign_role_to_user, set_password, get_role_info, add_user_to_auth_service, delete_user_to_auth_service, get_user_info, get_user_info2, update_user_to_auth_service

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from utils.views import BaseViewSet
from utils.roles import UsuariosRoles
from utils.logs_config import log_exception

from usuarios.models import User, UserDocument, UserPhoto, UserAudio
from usuarios.serializers import UserSerializer, UserCreateSerializer, UserDocumentSerializer, UserPhotoSerializer, UserAudioSerializer


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
                try:
                    delete_user_to_auth_service(user_auth_service_id)
                except Exception as rollback_error:
                    log_exception('create (rollback)', rollback_error)
                    return Response({'message': 'Falha no rollback do Keycloak', 'errors': str(rollback_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            log_exception('create', e)
            return Response({'message': 'Create failed!', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            
            if any(role in self.roles_required['destroy_total'] for role in request.roles) or str(request.current_user_id) == pk:

                with transaction.atomic():

                    user = get_object_or_404(self.queryset, id=pk)

                    # Deletar usuário do keycloak
                    user_auth_service_id = get_user_info(username=user.username)
                    delete_user_to_auth_service(user_auth_service_id)

                    # Deletar usuário do Django
                    user.delete()
                   
                    return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)         
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        except Http404:
            return Response({"detail": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_exception('destroy', e)
            return Response({"detail": f"An unexpected error occurred22. {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_total'] for role in request.roles):
                list_users = self.filter_queryset(self.queryset)
                list_serializer = self.serializer_class(list_users, many=True)
                return Response({'usuários': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                user = get_object_or_404(self.queryset, id=request.current_user_id)
                user_serializer = self.serializer_class(user)
                return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)
        
        except Http404:
            return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_exception('list', e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            
            if not (any(role in self.roles_required['list_total'] for role in request.roles) or str(request.current_user_id) == pk):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(self.queryset, id=pk)
            user_serializer = self.serializer_class(user)
            return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)

        except Http404:
            return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_exception('retrieve', e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            pk = kwargs.get('pk')

            if not (any(role in self.roles_required['list_total'] for role in request.roles) or str(request.current_user_id) == pk):
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
                    log_exception('partial_update (rollback)', rollback_error)
                    return Response({'message': 'Falha no rollback do Keycloak', 'errors': str(rollback_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            log_exception('partial_update', e)
            return Response({'message': 'Create failed!', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            pk = kwargs.get('pk')
            

            if not (any(role in self.roles_required['list_total'] for role in request.roles) or str(request.current_user_id) == pk):
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
                    log_exception('update (rollback)', rollback_error)
                    return Response({'message': 'Falha no rollback do Keycloak', 'errors': str(rollback_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            log_exception('update', e)
            return Response({'message': 'Create failed!', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_password(self, request, *args, **kwargs):
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

            if not (any(role in self.roles_required['update_password_total']  for role in request.roles) or str(request.current_user_id) == pk):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(self.queryset, id=pk)
            set_password(user.auth_service_id, password)
            
            return Response({'message': 'Update successful!'}, status=status.HTTP_200_OK)
        
        except Http404:
            return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log_exception('update_password', e)
            return Response({"detail": "An unexpected error occurred.", 'errors':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
