import uuid

from django.db import models

from utils.models import Base
from utils.validations import StructureValidators

class User(Base):
    class Role(models.TextChoices):
        MEDICO_VET = 'médico veterinário'
        GROOMER = 'groomer'
        ATENDENTE = 'atendente'
        ASSIS_VET = 'assistente veterinario'
        ESTAGIARIO = 'estagiario'
        CAIXA = 'caixa'
        ZELADOR = 'zelador'
        ENTREGADOR = 'entregador'
        OUTRO = 'outro'

    class Area(models.TextChoices):
        SAUDE = 'saude'
        HOTEL = 'hotel'
        BANHOTOSA = 'banho/tosa'
        LOJA = 'loja'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[StructureValidators.phone_validator])
    role = models.CharField(choices=Role.choices, max_length=50)
    area = models.CharField(choices=Area.choices, max_length=50)

    def __str__(self):
        return f'{self.name} ({self.role})'

class UserDocument(Base):
    class Type(models.TextChoices):
        CNPJ = 'cnpj'
        CPF = 'cpf'
        RG = 'rg'
        CRMV = 'crmv'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    doc_type = models.CharField(choices=Type.choices, max_length=50)
    doc_number = models.CharField(max_length=50)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name='documents', editable=False)

    def clean(self):
        super().clean()

        if self.doc_type == self.Type.CPF:
            StructureValidators.cpf_validator(self.doc_number)

    def save(self, *args, **kwargs):
        self.clean()  # Chama a validação antes de salvar
        super().save(*args, **kwargs)

class UserPhoto(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    photo_path = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', editable=False)

class UserAudio(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    audio_path = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios', editable=False)
