from utils.logs_config import log_exception

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

class KeycloakRollBackError(Exception):
    """
    Exceção personalizada para validação no upload de áudio.
    Já possui o log configurado.
    """
    def __init__(self, message="Falha no rollback do Keycloak'"):
        self.message = message
        log_exception('KeycloakRollBackError', message)
        super().__init__(self.message)
        