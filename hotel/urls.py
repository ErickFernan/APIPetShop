from rest_framework import routers
from django.urls import path, include

from hotel.views import ReservationViewSet, ServiceViewSet, ReservationServiceViewSet

router = routers.DefaultRouter()
router.register(r'reservation', ReservationViewSet, basename='reservation')
router.register(r'service', ServiceViewSet, basename='service')
router.register(r'reservationservice', ReservationServiceViewSet, basename='reservationservice')

urlpatterns = [
    path('', include(router.urls)),
]
