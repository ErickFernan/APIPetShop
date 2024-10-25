import uuid

from django.db import models

from utils.models import BaseModel
from usuarios.models import User


class Specie(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class Breed(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    habits = models.TextField(blank=True, null=True)
    nutrition =  models.TextField(blank=True, null=True)
    recommended_environment = models.TextField(blank=True, null=True)
    average_lifespan_years = models.PositiveSmallIntegerField(blank=True, null=True) 
    species_id = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name='breeds', editable=False)
    
    def __str__(self):
        return f'{self.name}'

class Pet(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    photo_path = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    pet_owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets_owned', editable=False)
    breed_id = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='pets', editable=False)

    def __str__(self):
        return f'{self.name} ({self.breed_id.name})'
