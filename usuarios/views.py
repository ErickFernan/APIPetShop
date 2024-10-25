from utils.views import BaseViewSet
from utils.roles import PRODUCTS_ROLES

from usuarios.models import User, UserDocument, UserPhoto, UserAudio
from usuarios.serializers import UserSerializer, UserDocumentSerializer, UserPhotoSerializer, UserAudioSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    roles_required = PRODUCTS_ROLES

class UserDocumentViewSet(BaseViewSet):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer
    roles_required = PRODUCTS_ROLES

class UserPhotoViewSet(BaseViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = UserPhotoSerializer
    roles_required = PRODUCTS_ROLES

class UserAudioViewSet(BaseViewSet):
    queryset = UserAudio.objects.all()
    serializer_class = UserAudioSerializer
    roles_required = PRODUCTS_ROLES
