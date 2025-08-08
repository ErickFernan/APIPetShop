from rest_framework import serializers

from loja.models import Sale, SaleProduct

from django.shortcuts import get_object_or_404

from usuarios.models import User


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'

class SaleCreateSerializer(serializers.ModelSerializer): # Criado para não permitir a edição dos ids no update depois de criado
    seller_id = serializers.UUIDField(write_only=True)
    purchase_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        seller_id = validated_data.pop('seller_id')
        purchase_id = validated_data.pop('purchase_id')

        seller = get_object_or_404(User, id=seller_id)
        purchase = get_object_or_404(User, id=purchase_id)

        return Sale.objects.create(
            seller_id=seller,
            purchase_id=purchase,
            **validated_data
        )

class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = '__all__'

