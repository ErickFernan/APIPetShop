from utils.views import BaseViewSet
from utils.roles import PRODUCTS_ROLES

from loja.models import Sale, SaleProduct
from loja.serializers import SaleSerializer, SaleProductSerializer


class SaleViewSet(BaseViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    roles_required = PRODUCTS_ROLES

class SaleProductViewSet(BaseViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer
    roles_required = PRODUCTS_ROLES
