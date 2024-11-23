from utils.logs_config import log_exception

from django.http import Http404
from django.db.utils import IntegrityError

from minio.error import S3Error

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status


class ImageValidationError(Exception):
    """
    Exception personalizada para validação no upload da imagem
    Já possui o log configurado
    """
    def __init__(self, message="The uploaded image format is invalid, unsupported, or corrupted. Please verify your file and upload a valid image file [JPEG or PNG]."):
        self.message = message
        log_exception('ImageValidationError', message)
        super().__init__(self.message)


class AudioValidationError(Exception):
    """
    Exceção personalizada para validação no upload de áudio.
    Já possui o log configurado.
    """
    def __init__(self, message="The uploaded audio format is invalid, unsupported, or corrupted. Please verify your file and upload a valid audio file [MP3 or WAV]."):
        self.message = message
        log_exception('AudioValidationError', message)
        super().__init__(self.message)


class KeycloakRollbackError(Exception):
    """
    Exceção personalizada para rollback do keycloak.
    Já possui o log configurado.
    """
    def __init__(self, message="Falha no rollback do Keycloak'"):
        self.message = message
        log_exception('KeycloakRollBackError', message)
        super().__init__(self.message)


# Função para logar exceções e gerar respostas padronizadas
def manage_exceptions(exception, context=''):
    """
    Centraliza o tratamento de exceções para todas as views. 
    Registra o erro e retorna uma resposta adequada ao cliente.
    """
    log_exception(context, exception)

    if isinstance(exception, IntegrityError):
        return Response({'message': "Erro de integridade.", "details": str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, ValidationError):
        return Response({'message': "Erro de validação.", "details": exception.detail}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, ImageValidationError):
        return Response({'message': "Invalid image file.", "details" : str(exception)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exception, AudioValidationError):
        return Response({'message': "Invalid audio file.", "details" : str(exception)}, status=status.HTTP_400_BAD_REQUEST)
    
    if isinstance(exception, Http404):
        return Response({"detail": "Arquivo não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exception, S3Error):
        return Response({"message": "upload_file", "detail": f"S3Error occurred: {exception.code} - {exception.message}", "errors": str(exception)}, status=status.HTTP_412_PRECONDITION_FAILED)

    return Response({"detail": "An unexpected error occurred.", "errors": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
