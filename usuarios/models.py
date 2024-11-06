import uuid

from django.db import models
from django.core.exceptions import ValidationError

from utils.models import BaseModel
from utils.validations import StructureValidators

class User(BaseModel):
    class Role(models.TextChoices):
        MEDICO_VET = 'medico_veterinario'
        GROOMER = 'groomer'
        ATENDENTE_SAUDE = 'atendente_saude'
        ATENDENTE_HOTEL = 'atendente_hotel'
        ATENDENTE_LOJA = 'atendente_loja'
        ATENDENTE_BANHOTOSA = 'atendente_banhotosa'
        ASSIST_VET = 'assistente_veterinario'
        ESTAGIARIO = 'estagiario'
        CAIXA = 'caixa'
        ZELADOR = 'zelador'
        ENTREGADOR = 'entregador'
        SUPERUSER = 'superuser'
        USER = 'user'
        OUTRO = 'outro'

    class Area(models.TextChoices):
        SAUDE = 'saude'
        HOTEL = 'hotel'
        BANHOTOSA = 'banho/tosa'
        LOJA = 'loja'
        USER = 'user'
        GERAL = 'geral'
        SUPERUSER = 'superuser'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, validators=[StructureValidators.phone_validator])
    role = models.CharField(choices=Role.choices, max_length=50)
    area = models.CharField(choices=Area.choices, max_length=50)
    auth_service_id = models.UUIDField(editable=False, unique=True)
    username = models.CharField(max_length=25, unique=True, editable=False, validators=[StructureValidators.username_validator])

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role})'

    def clean(self):
        valid_roles = {
            self.Area.SAUDE: {
                self.Role.MEDICO_VET,
                self.Role.ATENDENTE_SAUDE,
                self.Role.ASSIST_VET,
                self.Role.ESTAGIARIO,
                self.Role.CAIXA,
                self.Role.ZELADOR,
            },
            self.Area.HOTEL: {
                self.Role.ATENDENTE_HOTEL,
                self.Role.CAIXA,
                self.Role.ZELADOR,
                self.Role.ESTAGIARIO,
            },
            self.Area.BANHOTOSA: {
                self.Role.GROOMER,
                self.Role.ATENDENTE_BANHOTOSA,
                self.Role.ESTAGIARIO,
                self.Role.CAIXA,
                self.Role.ZELADOR,
                self.Role.ENTREGADOR,
            },
            self.Area.LOJA: {
                self.Role.ATENDENTE_LOJA,
                self.Role.ESTAGIARIO,
                self.Role.CAIXA,
                self.Role.ZELADOR,
                self.Role.ENTREGADOR,
            },
            self.Area.USER: {self.Role.USER},
            self.Area.SUPERUSER: {self.Role.SUPERUSER},
        }

        if self.role not in valid_roles.get(self.area, set()):
            raise ValidationError(f"A função '{self.role}' não é permitida na área '{self.area}'.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class UserDocument(BaseModel):
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


class UserPhoto(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    photo_path = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', editable=False)


class UserAudio(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    audio_path = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios', editable=False)
