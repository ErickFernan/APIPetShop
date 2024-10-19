from django.db import models

from usuarios.models import User
class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50)
    birthday = models.DateField()
    photo_path = models.CharField(max_length=100, blank=True, null=True)
    weight = models.PositiveSmallIntegerField()
    pet_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)

class Species(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    recommended_environment = models.TextField(blank=True, null=True)

class Breed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    habits = models.TextField(blank=True, null=True)
    nutrition =  models.TextField(blank=True, null=True)
    average_lifespan_years = models.PositiveIntegerField(blank=True, null=True) 
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='breeds')
