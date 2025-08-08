from rest_framework import serializers

from produtos.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # exclude = ['photo_path']

class ProductSerializerLimited(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'sale_price', 'stock', 'photo_path', 'product_type', 'expiration_date']
        