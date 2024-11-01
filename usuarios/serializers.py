from rest_framework import serializers

from usuarios.models import User, UserDocument, UserPhoto, UserAudio


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    keycloak_id = serializers.UUIDField(required=False, write_only=True)
    class Meta:
        model = User
        fields = '__all__'

class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = '__all__'

class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = '__all__'

class UserAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAudio
        fields = '__all__'
