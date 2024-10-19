from PIL import Image


def image_validation(file):
    try:
        with Image.open(file) as img:
            img.verify()
            if img.format not in ['JPEG', 'PNG']:
                return False, "The file must be a JPEG or PNG image."
            return True, None
                
    except (IOError, SyntaxError) as e:
        return False, "The uploaded file is not a valid image."
