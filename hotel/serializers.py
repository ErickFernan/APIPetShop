from rest_framework import serializers

from hotel.models import Reservation, Service, ReservationService


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        ref_name = 'HotelService'

class ReservationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationService
        fields = '__all__'
