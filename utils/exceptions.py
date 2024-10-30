class ImageValidationError(Exception):
    """Exception personalizada para validação no uplado da imagem"""
    def __init__(self, message="The uploaded image format is invalid or unsupported. Please upload a valid image file [JPEG or PNG]."):
        self.message = message
        super().__init__(self.message)
