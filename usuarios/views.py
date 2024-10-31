from keycloak import KeycloakOpenIDConnection
from keycloak_config.keycloak_client import assign_role_to_user, keycloak_admin, set_password

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

                    user = serializer.save()

                    user_id = keycloak_admin.create_user({
                        "username": user.email,
                        "email": user.email,
                        "enabled": True,
                        "firstName": user.first_name,
                        "lastName": user.last_name,
                        "attributes": {
                            "locale": ["pt-BR"]
                        }
                    },
                    exist_ok=False)

                    assign_role_to_user(user_id, user.role)
                    set_password(user_id, password)
                    
                    return Response({'message': 'Create successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Create failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Erro: {e}")
            return Response({'message': 'Create failed!', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            user = get_object_or_404(self.queryset, id=pk)
            
            if any(role in self.roles_required['destroy_total'] for role in request.roles) or request.current_user == user.email:

                with transaction.atomic():

                    # Deletar usuário do keycloak
                    user_id_keycloak = keycloak_admin.get_user_id(user.email)
                    response = keycloak_admin.delete_user(user_id=user_id_keycloak)

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
            list_users = self.filter_queryset(self.queryset)
            if any(role in self.roles_required['list_total'] for role in request.roles):
                list_serializer = self.serializer_class(list_users, many=True)
                return Response({'usuários': list_serializer.data}, status=status.HTTP_200_OK)

            # elif request.current_user == user.email:
            else:
                user = get_object_or_404(self.queryset, email=request.current_user)
                user_serializer = self.serializer_class(user)
                return Response({'usuário': user_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
