from utils.views import BaseViewSet
from utils.roles import PRODUCTS_ROLES

from pet.models import Specie, Breed, Pet
from pet.serializers import SpecieSerializer, BreedSerializer, PetSerializer


class SpecieViewSet(BaseViewSet):
    queryset = Specie.objects.all()
    serializer_class = SpecieSerializer
    roles_required = PRODUCTS_ROLES

class BreedViewSet(BaseViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    roles_required = PRODUCTS_ROLES

class PetViewSet(BaseViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    roles_required = PRODUCTS_ROLES

    folder_prefix = 'pets'
