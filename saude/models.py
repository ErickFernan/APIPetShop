import uuid

from django.db import models
from rest_framework.exceptions import ValidationError

from utils.models import BaseModel
from usuarios.models import User
from pet.models import Pet


class TreatmentCycle(BaseModel):
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

    class Meta:
        unique_together = ('pet_id', 'start_date')

    def __str__(self):
        return f'{self.pet_id.name} ({self.status})'

class Service(BaseModel):
    class Type(models.TextChoices):
        CONSULTA = 'consulta'
        EXAME = 'exame'
        CIRUGIA = 'cirurgia'
        VACINA = 'aplicacao de vacina'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    responsible_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responsible_services', editable=False)
    assistant_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assistant_services', blank=True, null=True)
    service_type = models.CharField(choices=Type.choices, max_length=50)
    description = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    start_date = models.DateField(editable=False)
    return_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    cycle_id = models.ForeignKey(TreatmentCycle, on_delete=models.CASCADE, related_name='related_services', editable=False)

    def __str__(self):
        return f'{self.service_type} ({self.responsible_id})'

    def clean(self):
        super().clean()

        # Verifica se o assistente é diferente do responsável
        if self.assistant_id and self.assistant_id == self.responsible_id:
            raise ValidationError("O assistente não pode ser o mesmo que o responsável.")

        # Verifica se o papel do assistente é válido
        if self.assistant_id:
            valid_assistant_roles = {
                User.Role.ATENDENTE_SAUDE,
                User.Role.ASSIST_VET,
                User.Role.ESTAGIARIO,
            }

            if self.assistant_id.role not in valid_assistant_roles:
                raise ValidationError(f"O assistente deve ter um dos papéis: {', '.join(valid_assistant_roles)}.")

        # Verifica se o papel do responsavel é válido
        if self.responsible_id:
            valid_responsible_roles = {
                User.Role.MEDICO_VET
                # Aqui devo colocar outros quando o sistema crescer, por exemplo um profissional de raiox, ressonancia, fisioterapeuta etc...
                # Caso o sistema cresca, pode-se fazer a mesma verificação que fiz nos usuário, permitindo apenas combinações especificas de responsável e assistente, mas por enquanto esta é suficiente.
            }

            if self.responsible_id.role not in valid_responsible_roles:
                    raise ValidationError(f"O responsável deve ter um dos papéis: {', '.join(valid_responsible_roles)}.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Usa full_clean() para validar os campos e o modelo
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('responsible_id', 'cycle_id')

class ExamType(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class Exam(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    exam_type_id = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='exams', editable=False)
    result_path = models.CharField(max_length=100, blank=True, null=True)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='related_exams', editable=False)

    def __str__(self):
        return f'{self.exam_type_id.name} ({self.service_id.cycle_id.pet_id.name})'
