from rest_framework import serializers

from hotel.models import Reservation, Service, ReservationService

from django.shortcuts import get_object_or_404

from usuarios.models import User

from pet.models import Pet



class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class ReservationCreateSerializer(serializers.ModelSerializer): # Criado para não permitir a edição dos ids no update depois de criado
    seller_id = serializers.UUIDField(write_only=True)
    pet_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        seller_id = validated_data.pop('seller_id')
        pet_id = validated_data.pop('pet_id')

        seller = get_object_or_404(User, id=seller_id)
        pet = get_object_or_404(Pet, id=pet_id)

        return Reservation.objects.create(
            seller_id=seller,
            pet_id=pet,
            **validated_data
        )

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        ref_name = 'HotelService'

class ReservationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationService
        fields = '__all__'
