from rest_framework import serializers

from usuarios.models import User, UserDocument, UserPhoto, UserAudio


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        # fields = '__all__'
        # Pesquisando como faria pra ocultar campos de uma classe extendida. Não sei se vou usar no resto do projeto ¯\_(ツ)_/¯.
        fields = [field.name for field in User._meta.fields if field.name not in ('created_at', 'updated_at')]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    auth_service_id = serializers.UUIDField(required=False, write_only=True)
    username = serializers.CharField(required=True, write_only=True)
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
