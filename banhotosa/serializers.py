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

        # buscar os objetos para validação
        func = get_object_or_404(User, id=func_id)
        pet = get_object_or_404(Pet, id=pet_id)

        # criar uma cópia do data para montar o Appointment
        appointment_data = data.copy()
        appointment_data["func_id"] = func
        appointment_data["pet_id"] = pet

        appointment = Appointment(**appointment_data)

        if isinstance(appointment.appointment_time, str):
            appointment.appointment_time = datetime.strptime(appointment.appointment_time, "%H:%M").time()

        validate_appointment_conflict(appointment)

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
        