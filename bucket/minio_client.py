from minio import Minio # Poderia usar o boto3, mas preferi o do próprio minio
from minio.error import S3Error

from django.conf import settings

from utils.logs_config import handle_exception

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)

def upload_file(file_data, file_name, content_type, folder_prefix):
    """
    Função responsável pelo envio de arquivos para o Minio
    """
    try:
        if not minio_client.bucket_exists(settings.MINIO_BUCKET_NAME):
            minio_client.make_bucket(settings.MINIO_BUCKET_NAME)

        file_data.seek(0) # Reposiciona o ponteiro do arquivo para o início
        length = file_data.size 

        minio_client.put_object(
            settings.MINIO_BUCKET_NAME,
            f"{folder_prefix}/{file_name}",
            file_data,
            length=length,
            # part_size=10*1024*1024,
            content_type=content_type,
        )
        # print(f"{folder_prefix}/{file_name}")
        return True

    except S3Error as e:
        log_exception('upload_file', f"S3Error occurred: {e.code} - {e.message}")
        return False

    except Exception as e:
        handle_exception('upload_file', e)
        return False

def delete_file(full_name):
    """
    Função responsável pela deleção de arquivos no Minio
    """
    try:
        minio_client.remove_object(
            settings.MINIO_BUCKET_NAME,
            f"{full_name}",
        )
        print(settings.MINIO_BUCKET_NAME+'/'+full_name)
        return True
    
    except S3Error as e: # Depois adicionar essa exception ao arquivo de exceptions e padronizar a saida
        log_exception('delete_file', f"S3Error occurred: {e.code} - {e.message}")
        return False

    except Exception as e:
        handle_exception('delete_file', e)
        return False

def delete_list_files(objects_name_list):
    """
    Função responsável pela deleção de uma lista de arquivos no Minio
    """
    try:
        a=map(delete_file, objects_name_list)
        print(list(a))

    except Exception as e:
        handle_exception('delete_list_files', e)
        return False
