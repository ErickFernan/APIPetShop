from utils.logs_config import log_exception

class ImageValidationError(Exception):
    """
    Exception personalizada para validação no upload da imagem
    Já possui o log configurado
    """
    def __init__(self, message="The uploaded image format is invalid or unsupported. Please upload a valid image file [JPEG or PNG]."):
        self.message = message
        log_exception('ImageValidationError', message)
        super().__init__(self.message)
