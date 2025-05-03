from rest_framework import routers
from django.urls import path, include

from banhotosa.views import AppointmentViewSet, ServiceTypeViewSet, ProductUsedViewSet, AppointmentServiceViewSet

router = routers.DefaultRouter()
router.register(r'appointment', AppointmentViewSet, basename='appointment')
router.register(r'service_type', ServiceTypeViewSet, basename='service_type')
router.register(r'product_used', ProductUsedViewSet, basename='product_used')
router.register(r'appointment_service', AppointmentServiceViewSet, basename='appointment_service')

urlpatterns = [
    path('', include(router.urls)),
]
