import uuid

from django.db import models

from utils.models import BaseModel
from pet.models import Pet
from usuarios.models import User


class Reservation(BaseModel):
    class Status(models.TextChoices):
        CANCELADO = 'cancelado'
        CONCLUIDO = 'concluido'
        ANDAMENTO = 'andamento'
        RESERVADO = 'reservado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_hotel', editable=False)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reservations', editable=False)
    status = models.CharField(choices=Status.choices, max_length=50)

    def __str__(self):
        return f'{self.pet_id.name} ({self.role})'

class Service(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    price_per_day = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class ReservationService(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reservation_services')
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='services')
    
    def __str__(self):
        return f'{self.reservation_id.pet_id.name} ({self.reservation_id.start_date}) ({self.service_id.name})'
        

"""
por enquanto essa estrutura vai ser usada apenas para o tempo de hospedagem, pois não sei o que um hotel pode oferecer a mais  ¯\_(ツ)_/¯.
entretando deixei a estrutura encaminhada se for necessário outros serviços. Para isso seria necessário retirar os dias de reservation e 
adicionar ele em ReservationService, pois ai cada serviço teria seu propio tempo e seria calculado o preço de acordo.
Só para reforçar, como nesse teste quero apenas que ele recrute um tipo de hospedagem (simples, cara, economica, etc..)
vou manter essa estrtura de tabelas, mas em uma outra abordagem pode ser necessário uma reconfiguração das mesmas.
Eu tenho ciência que nesse caso a tabela ReservationService não terá mta serventia, mas depois eu penso em outro serviços funcionando
em conjunto e faço os ajustes. É melhor eu manter ela pra futuramente ser usada, do que eu modificar agora e sair da normalização em uma futura att.
"""