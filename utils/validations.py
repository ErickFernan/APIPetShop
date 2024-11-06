from PIL import Image

from rest_framework import status
from rest_framework.response import Response

from datetime import time, timedelta

from django.core.validators import RegexValidator

from bucket.minio_client import upload_file

from utils.exceptions import ImageValidationError


def image_validation(file):
    """
    Valida se a imagem não está corrompida e se é um JPEG ou PNG
    """
    try:
        with Image.open(file) as img:
            img.verify()
            print(img.format)
            if img.format not in ['JPEG', 'PNG']:
                print('entreiaqui')
                raise ImageValidationError()
                
    except (IOError, SyntaxError) as e:
        raise ImageValidationError()


def validate_serializer_and_upload_file(serializer, file, file_name, content_type, folder_prefix):
    """
    Verifica se o serializer é válido, se for verifica se o file existe, se não existe ignora o if(verificação lazy),
    se existe verificar se o upload foi ok se foi ignora o if se não foi retorna erro.
    """
    if serializer.is_valid():
        if file and not upload_file(file, file_name, content_type, folder_prefix):
            return Response({"detail": "Failed to upload file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    
    print("Serializer errors:", serializer.errors)
    return Response({'message': 'Upload failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def appointment_time_validation(appointment_time, execution_time, close_time=22):
    """
    Esta função recebe o tempo que se deseja marcar o horário e o tempo necessario para concluir as tarefas
    e verifica se é possivel marcar e realizar o(s) serviço(s) naquele intervalo de tempo.
    """
    closing_time = time(close_time, 0)

    appointment_dt = timedelta(hours=appointment_time.hour, minutes=appointment_time.minute)
    execution_dt = timedelta(hours=execution_time.hour, minutes=execution_time.minute)

    total_time = appointment_dt + execution_dt

    return total_time <= timedelta(hours=closing_time.hour, minutes=closing_time.minute)

class StructureValidators():
    """
    Possiui algumas validação de estrutura utilizando Regex
    """
    cpf_validator = RegexValidator(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF inválido.')
    cnpj_validator = RegexValidator(r'^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$', message='CNPJ inválido.')
    rg_validator = RegexValidator(r'^\d{7,8}$', message='RG inválido. Deve ter entre 7 e 8 dígitos.')
    crmv_validator = RegexValidator(r'^\d{1,7}$', message='CRMV inválido. Deve ter entre 1 e 7 dígitos.')
    phone_validator = RegexValidator(r'^\(\d{2}\)\s\d{5}-\d{4}$', message='Número de telefone inválido')

    username_validator = RegexValidator(
        r'^(?!.*[_-]{2})(?![-_])(?=.{1,25}$)[A-Za-z0-9._-]+(?<![-_])$',
        message='Username inválido. Deve ter no máximo 25 caracteres, '
                'pode conter letras, números, ponto, sublinhado ou hífen, '
                'não pode começar ou terminar com um caractere especial, '
                'e não pode ter caracteres especiais consecutivos.'
    )
