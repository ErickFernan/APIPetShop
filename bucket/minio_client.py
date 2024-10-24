from minio import Minio # Poderia usar o boto3, mas preferi o do próprio minio
from minio.error import S3Error
from django.conf import settings


minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)

def upload_file(file_data, file_name, content_type, folder_prefix):
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
        print(f"{folder_prefix}/{file_name}")
        return True

    except S3Error as e:
        print(f"S3Error occurred: {e.code} - {e.message}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def delete_file(full_name):
    try:
        minio_client.remove_object(
            settings.MINIO_BUCKET_NAME,
            f"{full_name}",
        )
        return True
    
    except S3Error as e:
        print(f"S3Error occurred: {e.code} - {e.message}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred11: {e}")
        return False
