import uuid

from utils.models import Base
from django.db import models

class Product(Base):
    class Type(models.TextChoices):
        REMEDIO = 'remedio'
        PERFUMARIA = 'perfumaria'
        VACINA = 'vacina'
        VESTUARIO = 'vestuario'
        ALIMENTO = 'alimento'
        OUTRO = 'outro'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveSmallIntegerField()
    photo_path = models.CharField(max_length=100, blank=True, null=True)
    product_type = models.CharField(choices=Type.choices, max_length=50)
    storage_location = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.DateField()
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.name}, ({self.sale_price})'
        