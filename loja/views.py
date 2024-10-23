from rest_framework.viewsets import ModelViewSet

from loja.models import Sale, SaleProduct
from loja.serializers import SaleSerializer, SaleProductSerializer
class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleProductViewSet(ModelViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer
