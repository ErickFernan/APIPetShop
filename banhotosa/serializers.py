from rest_framework import serializers

from banhotosa.models import Appointment, ServiceType, ProductUsed


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ProductUsedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUsed
        fields = '__all__'
        