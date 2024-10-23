from rest_framework import serializers

from usuarios.models import User, UserDocument, UserPhoto, UserAudio


class UserSerializer(serializers.ModelSerializer):
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
        read_only_fields = ['photo_path']

class UserAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAudio
        fields = '__all__'
        read_only_fields = ['audio_path']
