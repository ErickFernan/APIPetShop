from rest_framework import serializers

from django.shortcuts import get_object_or_404

from banhotosa.models import Appointment, ServiceType, ProductUsed, AppointmentService

from usuarios.models import User

from pet.models import Pet

from datetime import datetime, timedelta

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

        if AppointmentService.objects.filter(appointment_id=appointment, service_type_id=service).exists():
            raise serializers.ValidationError("Este serviço já está associado a este agendamento.")
        print("appointment: ",appointment)
        print("service :",service)

        # Entre appointments diferentes ele está verificando corrreto?(pelo menos ta verificando) mas no mesmo appointment não, pois ele precisa calcular os horários daquel appointmente tb.

        # Dados do agendamento atual
        start_datetime = datetime.combine(appointment.date, appointment.appointment_time)
        duration = timedelta(hours=service.execution_time.hour, minutes=service.execution_time.minute)
        end_datetime = start_datetime + duration

        # Buscar outros agendamentos do mesmo funcionário no mesmo dia
        other_appointments = Appointment.objects.filter(
            date=appointment.date,
            func_id=appointment.func_id
        ).exclude(id=appointment.id)
        print("other_appointments: ",other_appointments)

        for appt in other_appointments:
            appt_start = datetime.combine(appt.date, appt.appointment_time)

            # Somar duração total dos serviços desse outro agendamento
            related_services = AppointmentService.objects.filter(appointment_id=appt.id)
            total_minutes = sum([
                s.service_type_id.execution_time.hour * 60 + s.service_type_id.execution_time.minute
                for s in related_services
            ])
            appt_end = appt_start + timedelta(minutes=total_minutes)

            # Verificar sobreposição
            if start_datetime < appt_end and end_datetime > appt_start:
                raise serializers.ValidationError("Conflito de horário com outro atendimento.")

        return data

        
class ProductUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUsed
        fields = '__all__'
        