import uuid

from utils.models import Schedules

from django.db import models
from utils.models import Base
from pet.models import Pet
from usuarios.models import User
from produtos.models import Product


class Appointment(Base):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments', editable=False)
    func_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', editable=False)
    appointment_time = models.TimeField(choices=Schedules.choices)
    date = models.DateField()

    def __str__(self):
        return f'{self.pet_id.name} ({self.appointment_time})'

class ServiceType(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='service_types', editable=False)
    name = models.CharField(max_length=50, unique=True)
    execution_time = models.TimeField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    product_used_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='service_types', editable=False)

    def __str__(self):
        return f'{self.name}'

class ProductUsed(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    service_type_id = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='products_used', editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='used_in_services', editable=False)

    def __str__(self):
        return f'{self.service_type_id.name} ({self.product_id.name})'