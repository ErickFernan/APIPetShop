from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from usuarios.models import User, UserDocument, UserPhoto, UserAudio
from usuarios.serializers import UserSerializer, UserDocumentSerializer, UserPhotoSerializer, UserAudioSerializer
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDocumentViewSet(ModelViewSet):
    queryset = UserDocument.objects.all()
    serializer_class = UserDocumentSerializer

class UserPhotoViewSet(ModelViewSet):
    queryset = UserPhoto.objects.all()
    serializer_class = UserPhotoSerializer

class UserAudioViewSet(ModelViewSet):
    queryset = UserAudio.objects.all()
    serializer_class = UserAudioSerializer
