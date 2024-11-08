import os
import uuid
import logging

from django.http import Http404

from datetime import time, timedelta

from rest_framework.response import Response
from rest_framework import status

from utils.exceptions import ImageValidationError, AudioValidationError
from utils.logs_config import log_exception

def generate_time_choices(start_hour=6, end_hour=22, interval_minutes=30):
    """
    Gera uma lista de horários baseado no tempo funcionamento do estabelecimento e de um intervalo
    padrão pré-definido, em resumo se assemelha aos horários para marcação de uma agenda física 
    """
    times = []
    current_time = time(start_hour, 0)
    end_time = time(end_hour, 0)
    
    while current_time <= end_time:
        time_label = current_time.strftime('%H:%M')
        times.append((current_time, time_label))
        
        current_datetime = (timedelta(hours=current_time.hour, minutes=current_time.minute) 
                            + timedelta(minutes=interval_minutes))
        current_time = (time(current_datetime.seconds // 3600, 
                             (current_datetime.seconds // 60) % 60))
        
    return times

def convert_hours_units_to_time(unit):
    """
    Transforma unidades de tempo em horas e minutos,
    neste caso está prefedinido que o inteiro representa 30 min
    """
    if unit < 0 or unit > 32:
        raise ValueError("O número deve ser um inteiro positivo menor que 32.")
    
    total_minutes = unit * 30
    hours, minutes = divmod(total_minutes, 60)

    return time(hours, minutes)

def change_file_name(file_name):
    """
    troca o nome do arquivo original por um uuid
    """
    return f'({uuid.uuid4()}.{os.path.splitext(file_name)[1]})'

def extract_file_details(file, product=None):
    """
    Retira informações referentes ao arquivo enviado para que o minio possa utilizar
    """
    file_name = product.photo_path.split('/')[-1] if product and product.photo_path else change_file_name(file.name)
    content_type = file.content_type
    return file_name, content_type

# Função para logar exceções e gerar respostas padronizadas
def manage_exceptions(exception, context=''):
    """
    Centraliza o tratamento de exceções para todas as views. 
    Registra o erro e retorna uma resposta adequada ao cliente.
    """
    log_exception(context, exception)

    if isinstance(exception, ImageValidationError):
        return Response({'message': "Invalid image file.", "details" : str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, AudioValidationError):
        return Response({'message': "Invalid audio file.", "details" : str(exception)}, status=status.HTTP_400_BAD_REQUEST)
    
    elif isinstance(exception, Http404):
        return Response({"detail": "User não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({"detail": "An unexpected error occurred.", "errors": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
