import uuid

from django.db import models

from utils.models import BaseModel
from usuarios.models import User
from produtos.models import Product


class Sale(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_sales', editable=False)
    purchase_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_sales', editable=False)

    def __str__(self):
        return f'seller: {self.seller_id.name} purchase: ({self.purchase_id.name})'

class SaleProduct(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    sale_id = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='sale_products')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sale_products')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.product_id} ({self.quantity})'
