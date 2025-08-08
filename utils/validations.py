from PIL import Image

from pydub import AudioSegment
import magic

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from datetime import time, timedelta, datetime

from django.core.validators import RegexValidator

from bucket.minio_client import upload_file

from utils.exceptions import ImageValidationError, AudioValidationError, ImagePDFValidationError
from utils.logs_config import handle_exception

from django.apps import apps # Isso é importante para evitar importações diretas, ficar atento é algo muito importante


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
    

# pip install PyPDF2

from PIL import Image
import magic
from PyPDF2 import PdfReader
# from django.core.exceptions import ValidationError

def pdf_image_validation(file):
    """
    Valida se o arquivo é uma imagem (JPEG/PNG) ou um PDF válido.
    - Para imagens: verifica tipo MIME e se está corrompida.
    - Para PDFs: tenta abrir e acessar metadados com PyPDF2.
    """
    try:
        mime = magic.from_buffer(file.read(1024), mime=True)
        file.seek(0)

        if mime not in ['image/jpeg', 'image/png', 'application/pdf']:
            raise ImageValidationError()

        if mime in ['image/jpeg', 'image/png']:
            with Image.open(file) as img:
                img.verify()  # Confirma se imagem está corrompida
            file.seek(0)

        elif mime == 'application/pdf':
            try:
                reader = PdfReader(file)
                _ = reader.metadata  # Tenta acessar metadados como teste
            except Exception:
                raise ImageValidationError()
            file.seek(0)

    except Exception as e:
        raise ImagePDFValidationError()


def validate_serializer_and_upload_file(serializer, file=None, file_name=None, content_type=None, folder_prefix=None, user=None): # conferir se não quebrou nada colocar os nones
    """
    Valida o serializer e realiza o upload do arquivo.
    - Se o serializer for válido, verifica se o arquivo existe.
    - Se o arquivo existe, tenta fazer o upload. Se falhar, retorna erro.
    - Caso o upload seja bem-sucedido, salva o serializer e retorna sucesso.
    - Em caso de erro inesperado, captura a exceção e retorna erro genérico.
    """
    try:
        if serializer.is_valid():
        # if serializer.is_valid(raise_exception=True): # TESTAR ESSE QUANDO CHEGAR(AVALIAR SE É A MELHOR OPÇÃO para usar o transaction.atomic)

            if file and not upload_file(file, file_name, content_type, folder_prefix):

                return Response({"detail": "Failed to upload file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)

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


def validate_appointment_conflict(appointment, new_services=None):
    """
    Verifica conflitos de horário com base nos serviços de um appointment.

    :param appointment: Objeto Appointment (com date, appointment_time, func_id)
    :param new_services: Lista de instâncias de ServiceType (serviços novos)
    :raise ValidationError: se houver conflito de horário
    """
    Appointment = apps.get_model('banhotosa', 'Appointment')
    AppointmentService = apps.get_model('banhotosa', 'AppointmentService')

    appointment_start = datetime.combine(appointment.date, appointment.appointment_time)

    existing_services = AppointmentService.objects.filter(appointment_id=appointment)
    total_minutes = sum([
        s.service_type_id.execution_time.hour * 60 + s.service_type_id.execution_time.minute
        for s in existing_services
    ])

    if new_services:
        total_minutes += sum([
            s.execution_time.hour * 60 + s.execution_time.minute
            for s in new_services
        ])

    if total_minutes == 0:
        total_minutes = 30  # fallback

    appointment_end = appointment_start + timedelta(minutes=total_minutes)

    other_appointments = Appointment.objects.filter(
        date=appointment.date,
        func_id=appointment.func_id
    ).exclude(id=appointment.id)
    
    for appt in other_appointments:
        appt_start = datetime.combine(appt.date, appt.appointment_time)

        appt_services = AppointmentService.objects.filter(appointment_id=appt)
        appt_total_minutes = sum([
            s.service_type_id.execution_time.hour * 60 + s.service_type_id.execution_time.minute
            for s in appt_services
        ])
        if appt_total_minutes == 0:
            appt_total_minutes = 30

        appt_end = appt_start + timedelta(minutes=appt_total_minutes)

        if appointment_start < appt_end and appointment_end > appt_start:
            raise ValidationError("Conflito de horário com outro agendamento.")
        