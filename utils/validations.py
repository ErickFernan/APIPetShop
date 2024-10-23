from PIL import Image

from datetime import time, timedelta
from django.core.validators import RegexValidator


def image_validation(file):
    try:
        with Image.open(file) as img:
            img.verify()
            if img.format not in ['JPEG', 'PNG']:
                return False, "The file must be a JPEG or PNG image."
            return True, None
                
    except (IOError, SyntaxError) as e:
        return False, "The uploaded file is not a valid image."

def appointment_time_validation(appointment_time, execution_time):
    closing_time = time(22, 0)

    appointment_dt = timedelta(hours=appointment_time.hour, minutes=appointment_time.minute)
    execution_dt = timedelta(hours=execution_time.hour, minutes=execution_time.minute)

    total_time = appointment_dt + execution_dt

    return total_time <= timedelta(hours=closing_time.hour, minutes=closing_time.minute)

class StructureValidators():
    cpf_validator = RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF inválido.')
    cnpj_validator = RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', message='CNPJ inválido.')
    rg_validator = RegexValidator(r'^\d{7,8}$', message='RG inválido. Deve ter entre 7 e 8 dígitos.')
    crmv_validator = RegexValidator(r'^\d{1,7}$', message='CRMV inválido. Deve ter entre 1 e 7 dígitos.')
    phone_validator = RegexValidator(r'^\(\d{2}\)\s\d{5}-\d{4}$', message='Número de telefone inválido')
