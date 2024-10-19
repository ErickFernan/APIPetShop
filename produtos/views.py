from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from produtos.models import Product
from produtos.serializers import ProductSerializer

from bucket.minio_client import upload_file

from utils.validacoes import image_validation

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request):
        try:
            data = request.data
            file = request.FILES.get('photo')

            if file:
                is_valid, message = image_validation(file=file)
                if not is_valid:
                    return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

                folder_prefix = 'products'
                file_name = file.name
                content_type = file.content_type

                upload_success = upload_file(file, file_name, content_type, folder_prefix)

                if upload_success:
                    data['photo_path'] = f"{folder_prefix}/{file_name}"
                else:
                    return Response({"detail": "Failed to upload file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print("Serializer errors:", serializer.errors)
                return Response({'message': 'Upload failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            