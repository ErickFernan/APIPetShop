from PIL import Image

from pydub import AudioSegment
import magic

from rest_framework import status
from rest_framework.response import Response

from datetime import time, timedelta

from django.core.validators import RegexValidator

from bucket.minio_client import upload_file

from utils.exceptions import ImageValidationError, AudioValidationError
from utils.logs_config import handle_exception


def image_validation(file):
    """
    Valida se a imagem não está corrompida e se é um JPEG ou PNG
    """
    try:
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0) # é necessário voltar o ponteiro pois consumi os primeiros 1024 bytes do arquivo
        if mime not in ['image/jpeg', 'image/png']:
            raise ImageValidationError()

        with Image.open(file) as img:
            img.verify()  # Verifica se a imagem está corrompida
                
    except Exception as e:
        raise ImageValidationError() # Optei pro mostrar um erro generico nos dois casos

def audio_validation(file):
    """
    Valida se o áudio não está corrompido e se é MP3 ou WAV.
    """
    try:
        # Verifique se o tipo MIME é MP3 ou WAV → muito mais seguro que usar .ext
        mime = magic.from_buffer(file.read(1024), mime=True)
        if mime not in ['audio/mpeg', 'audio/wav']:
            raise AudioValidationError()
        file.seek(0) # é necessário voltar o ponteiro pois consumi os primeiros 1024 bytes do arquivo
        
        AudioSegment.from_file(file) # Verifica se esta corrompido
    
    except Exception as e:
        raise AudioValidationError()

def validate_serializer_and_upload_file(serializer, file, file_name, content_type, folder_prefix, user=None):
    """
    Valida o serializer e realiza o upload do arquivo.
    - Se o serializer for válido, verifica se o arquivo existe.
    - Se o arquivo existe, tenta fazer o upload. Se falhar, retorna erro.
    - Caso o upload seja bem-sucedido, salva o serializer e retorna sucesso.
    - Em caso de erro inesperado, captura a exceção e retorna erro genérico.
    """
    try:
        print('ab')
        if serializer.is_valid():
            print('h')
            if file and not upload_file(file, file_name, content_type, folder_prefix):
                print('a')
                return Response({"detail": "Failed to upload file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)
            print('b')
            serializer.save(user_id=user) if user else serializer.save()
            return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'message': 'Upload failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        handle_exception('validate_serializer_and_upload_file', e)
        # A exception deve ser tratada na view

def appointment_time_validation(appointment_time, execution_time, close_time=22):
    """
    Esta função recebe o tempo que se deseja marcar o horário e o tempo necessario para concluir as tarefas
    e verifica se é possivel marcar e realizar o(s) serviço(s) naquele intervalo de tempo.
    """
    try:
        closing_time = time(close_time, 0)

        appointment_dt = timedelta(hours=appointment_time.hour, minutes=appointment_time.minute)
        execution_dt = timedelta(hours=execution_time.hour, minutes=execution_time.minute)

        total_time = appointment_dt + execution_dt

        return total_time <= timedelta(hours=closing_time.hour, minutes=closing_time.minute)

    except Exception as e:
        handle_exception('appointment_time_validation', e)
        # A exception deve ser tratada na view


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
