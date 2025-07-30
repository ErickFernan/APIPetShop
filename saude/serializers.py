from rest_framework import serializers

from saude.models import TreatmentCycle, Service, ExamType, Exam

from django.shortcuts import get_object_or_404

from pet.models import Pet

from usuarios.models import User


class TreatmentCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCycle
        fields = '__all__'

class TreatmentCycleCreateSerializer(serializers.ModelSerializer): # Criado para não permitir a edição dos ids no update depois de criado
    pet_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = TreatmentCycle
        fields = '__all__'

    def create(self, validated_data):
        pet_id = validated_data.pop('pet_id')

        pet = get_object_or_404(Pet, id=pet_id)

        return TreatmentCycle.objects.create(
            pet_id=pet,
            **validated_data
        )

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        ref_name = 'SaudeService'

class ServiceCreateSerializer(serializers.ModelSerializer): # Criado para não permitir a edição dos ids no update depois de criado
    responsible_id = serializers.UUIDField(write_only=True)
    start_date = serializers.DateField(write_only=True)
    ciclo_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        responsible_id = validated_data.pop('responsible_id')
        start_date = validated_data.pop('start_date')
        ciclo_id = validated_data.pop('ciclo_id')

        responsible = get_object_or_404(User, id=responsible_id)
        cicle = get_object_or_404(TreatmentCycle, id=ciclo_id)

        return Service.objects.create(
            responsible_id=responsible,
            start_date=start_date,
            ciclo_id=cicle,
            **validated_data
        )

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamCreateSerializer(serializers.ModelSerializer): # Criado para não permitir a edição dos ids no update depois de criado
    exam_type_id = serializers.UUIDField(write_only=True)
    service_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Exam
        fields = '__all__'

    def create(self, validated_data):
        exam_type_id = validated_data.pop('exam_type_id')
        service_id = validated_data.pop('service_id')

        exam = get_object_or_404(ExamType, id=exam_type_id)
        service = get_object_or_404(Service, id=service_id)

        return Exam.objects.create(
            exam_type_id=exam,
            service_id=service,
            **validated_data
        )
    