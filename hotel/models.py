import uuid

from django.db import models

from utils.models import BaseModel
from pet.models import Pet

class Reservation(BaseModel):
    class Status(models.TextChoices):
        CANCELADO = 'cancelado'
        CONCLUIDO = 'concluido'
        ANDAMENTO = 'andamento'
        RESERVADO = 'reservado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reservations', editable=False)
    status = models.CharField(choices=Status.choices, max_length=50)

    def __str__(self):
        return f'{self.pet_id.name} ({self.role})'

class Service(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    price_per_day = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class ReservationService(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reservation_services', editable=False)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='services', editable=False)

    def __str__(self):
        return f'{self.reservation_id.pet_id.name} ({self.reservation_id.start_date}) ({self.service_id.name})'
        