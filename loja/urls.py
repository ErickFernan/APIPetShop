from rest_framework import routers
from django.urls import path, include

from loja.views import SaleViewSet, SaleProductViewSet

router = routers.DefaultRouter()
router.register(r'sale', SaleViewSet, basename='sale')
router.register(r'sale_product', SaleProductViewSet, basename='sale_product')

urlpatterns = [
    path('', include(router.urls)),
]
