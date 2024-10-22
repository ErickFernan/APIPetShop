from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from pet.models import Specie, Breed, Pet
from pet.serializers import SpecieSerializer, BreedSerializer, PetSerializer
class SpecieViewSet(ModelViewSet):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer

class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
