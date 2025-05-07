import uuid


from rest_framework import serializers

from django.shortcuts import get_object_or_404

from banhotosa.models import Appointment, ServiceType, ProductUsed, AppointmentService

from usuarios.models import User

from pet.models import Pet

from datetime import datetime, timedelta

from utils.validations import validate_appointment_conflict


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class AppointmentCreateSerializer(serializers.ModelSerializer): # Criado para não permitir a edição dos ids no update depois de criado
    func_id = serializers.UUIDField(write_only=True)
    pet_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        func_id = validated_data.pop('func_id')
        pet_id = validated_data.pop('pet_id')

        func = get_object_or_404(User, id=func_id)
        pet = get_object_or_404(Pet, id=pet_id)

        return Appointment.objects.create(
            func_id=func,
            pet_id=pet,
            **validated_data
        )

    def validate(self, data):
        func_id = data.get("func_id")
        pet_id = data.get("pet_id")

        teste_func_id = data["func_id"]
        teste_pet_id = data["pet_id"]

        if isinstance(func_id, uuid.UUID):
            func = get_object_or_404(User, id=func_id)
            data["func_id"] = func
        if isinstance(pet_id, uuid.UUID):
            pet = get_object_or_404(Pet, id=pet_id)
            data["pet_id"] = pet

        appointment = Appointment(**data)

        appointment.appointment_time = datetime.strptime(appointment.appointment_time, "%H:%M").time() # preciso fazer isso pois ele chega como txt

        validate_appointment_conflict(appointment)

        data["func_id"] = teste_func_id
        data["pet_id"] = teste_pet_id

        return data


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class AppointmentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentService
        fields = '__all__'

    def validate(self, data):
        appointment = data['appointment_id']
        service = data['service_type_id']

        validate_appointment_conflict(appointment, new_services=[service])

        return data

        
class ProductUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUsed
        fields = '__all__'
        