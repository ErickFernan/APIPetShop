from keycloak import KeycloakOpenIDConnection
from keycloak_config.keycloak_client import assign_role_to_user, keycloak_admin, set_password

from django.db import transaction

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
        serializer = self.serializer_class(data=request.data)
        
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
