from rest_framework import routers
from django.urls import path, include

from produtos.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'produtos', ProductViewSet, basename='produtos')

urlpatterns = [
    path('', include(router.urls)),
]