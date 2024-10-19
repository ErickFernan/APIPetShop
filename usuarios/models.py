import uuid

from django.db import models
from django.core.validators import RegexValidator


class User(models.Model):
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
    cpf = models.CharField(max_length=14, validators=[RegexValidator(r'\d{3}\.\d{3}\.\d{3}-\d{2}', message='CPF inválido')], blank=True, null=True)
    phone = models.CharField(max_length=20, validators=[RegexValidator(r'^\(\d{2}\)\s\d{5}-\d{4}$', message='Número de telefone inválido')])
    role = models.CharField(choices=Role.choices, max_length=50)
    area = models.CharField(choices=Area.choices, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserDocument(models.Model):
    class Type(models.TextChoices):
        CNPJ = 'cnpj'
        RG = 'rg'
        CRMV = 'crmv'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    doc_type = models.CharField(choices=Type.choices, max_length=50)
    doc_number = models.CharField(max_length=50)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name='documents')

class UserPhoto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    photo_path = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')

class UserAudio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    audio_path = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios')
