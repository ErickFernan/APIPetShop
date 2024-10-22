import uuid

from django.db import models

from utils.models import Base
from usuarios.models import User
from pet.models import Pet


class TreatmentCycle(Base):
    class Status(models.TextChoices):
        CANCELADO = 'cancelado'
        CONCLUIDO = 'concluido'
        ANDAMENTO = 'andamento'
        AGENDADO  = 'agendado'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    pet_id = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='treatment_cycles', editable=False)
    complaits = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    dignosis = models.TextField(blank=True, null=True)
    status = models.CharField(choices=Status.choices, max_length=50)

    def __str__(self):
        return f'{self.pet_id.name} ({self.status})'

class Service(Base):
    class Type(models.TextChoices):
        CONSULTA = 'consulta'
        EXAME = 'exame'
        CIRUGIA = 'cirurgia'
        VACINA = 'aplicacao de vacina'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    responsible_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible_services', editable=False)
    assistant_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistant_services', editable=False, blank=True, null=True)
    service_type = models.CharField(choices=Type.choices, max_length=50)
    description = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    start_date = models.DateField(editable=False)
    return_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    ciclo_id = models.ForeignKey(TreatmentCycle, on_delete=models.CASCADE, related_name='related_services', editable=False)

    def __str__(self):
        return f'{self.service_type} ({self.responsible_id})'

class ExamType(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class Exam(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    exam_type_id = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='exams', editable=False)
    result_path = models.CharField(max_length=100, blank=True, null=True)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='related_exams', editable=False)

    def __str__(self):
        return f'{self.exam_type_id.name} ({self.service_id.ciclo_id.pet_id.name})'
