from utils.views import BaseViewSet
from utils.roles import LojaRoles

from loja.models import Sale, SaleProduct
from loja.serializers import SaleSerializer, SaleProductSerializer


class SaleViewSet(BaseViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    roles_required = LojaRoles.SALE_ROLES

class SaleProductViewSet(BaseViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer
    roles_required = LojaRoles.SALEPRODUCT_ROLES
