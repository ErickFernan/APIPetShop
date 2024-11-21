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
    doc_type = serializers.CharField(required=False, write_only=True)
    doc_number = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocument
        fields = '__all__'


class UserDocumentCreateSerializer(serializers.ModelSerializer):
    # user_id = serializers.UUIDField(required=False, write_only=True)
    class Meta:
        model = UserDocument
        fields = '__all__'


class UserPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhoto
        fields = '__all__'


class UserPhotoCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False, write_only=True) # Required não deveria ser True? Eu preciso verificar esse user_id na outras rotas, n lembro pq coloquei, mas acho q ele não é necessário
    photo_path = serializers.CharField(required=False)
    photo = serializers.FileField(required=True, write_only=True) 
    class Meta:
        model = UserPhoto
        fields = '__all__'
    
    def create(self, validated_data):
        # Remove 'photo' do validated_data antes de salvar → Neste caso não tem como fugir ¯\_(ツ)_/¯.
        validated_data.pop('photo')
        return super().create(validated_data)


class UserAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAudio
        fields = '__all__'

class UserAudioCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False, write_only=True)
    audio_path = serializers.CharField(required=False)
    audio = serializers.FileField(required=True, write_only=True) 
    class Meta:
        model = UserAudio
        fields = '__all__'
    
    def create(self, validated_data):
        # Remove 'photo' do validated_data antes de salvar → Neste caso não tem como fugir ¯\_(ツ)_/¯.
        validated_data.pop('audio')
        return super().create(validated_data)

