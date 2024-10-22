from rest_framework import routers
from django.urls import path, include

from pet.views import SpecieViewSet, BreedViewSet, PetViewSet

router = routers.DefaultRouter()
router.register(r'specie', SpecieViewSet, basename='specie')
router.register(r'breed', BreedViewSet, basename='breed')
router.register(r'pet', PetViewSet, basename='pet')

urlpatterns = [
    path('', include(router.urls)),
]
