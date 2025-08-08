import uuid

from utils.models import Schedules

from django.db import models
from utils.models import BaseModel
from pet.models import Pet
from usuarios.models import User
from produtos.models import Product


class Appointment(BaseModel):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments', editable=False)
    func_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', editable=False) # Vou manter esse editable pois o mesmo será feito automaticamente pelo back-end
    appointment_time = models.TimeField(choices=Schedules.choices)
    date = models.DateField()

    def __str__(self):
        return f'{self.pet_id.name} ({self.appointment_time})'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'appointment_time', 'func_id'], name='unique_date_func_appointment_time')
        ]
    
    
class ServiceType(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    execution_time = models.TimeField()
    base_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name}'
    

class AppointmentService(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    appointment_id = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="services")
    service_type_id = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name="appointments")
    charged_price = models.DecimalField(max_digits=5, decimal_places=2) # Esse preço é necessário para manter um histórico do preço, pois seria o preço salvo será aquele no momento da criação, o que vai permitir que o preço do serviço seja ajustado a qualquer momento sem prejudicar o histórico

    def __str__(self):
        return f'{self.appointment_id} ({self.service_type_id})'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['appointment_id', 'service_type_id'], name='unique_appointment_service')
        ]
    
class ProductUsed(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    service_type_id = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name='products_used')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='used_in_services')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.service_type_id.name} ({self.product_id.name})'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product_id', 'service_type_id'], name='unique_product_id_service_type_id')
        ]
    