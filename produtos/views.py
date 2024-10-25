from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from produtos.models import Product
from produtos.serializers import ProductSerializer

from bucket.minio_client import upload_file, delete_file

from utils.validations import image_validation
from utils.functions import change_file_name

from keycloak_config.authentication import KeyCloakAuthentication
from keycloak_config.permissions import HasRolePermission


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    authentication_classes = [KeyCloakAuthentication]
    permission_classes = [HasRolePermission]
    roles_required = {
        'list': ['produtos-basic', 'produtos-total'],
        'retrieve': ['person-admin', 'person-user'],
        'create': ['produtos-total'],
        'update': ['produtos-total'],
        'destroy': ['produtos-total']
    }

    folder_prefix = 'products'

    def create(self, request):
        try:
            data = request.data
            file = request.FILES.get('photo')

            if file:
                is_valid, message = image_validation(file=file)
                if not is_valid:
                    return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

                file_name = change_file_name(file.name)
                content_type = file.content_type

                upload_success = upload_file(file, file_name, content_type, self.folder_prefix)

                if upload_success:
                    data['photo_path'] = f"{self.folder_prefix}/{file_name}"
                else:
                    return Response({"detail": "Failed to update file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Update successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print("Serializer errors:", serializer.errors)
                return Response({'message': 'Update failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                product = self.queryset.get(id=pk)

                if product.photo_path:
                    delete_success = delete_file(product.photo_path)
                    if not delete_success:
                        raise Exception("Failed to delete the photo file.")

                product.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred22."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def partial_update(self, request, *args, **kwargs):
        try:
            data = request.data
            file = request.FILES.get('photo')
            pk = kwargs.get('pk')
            product = self.queryset.get(id=pk)

            if file:
                is_valid, message = image_validation(file=file)
                if not is_valid:
                    return Response({"detail": message}, status=status.HTTP_400_BAD_REQUEST)

                if product.photo_path:
                    file_name = product.photo_path.split('/')[-1]
                else:
                    file_name = change_file_name(file.name)

                content_type = file.content_type
                upload_success = upload_file(file, file_name, content_type, self.folder_prefix)

                if upload_success:
                    data['photo_path'] = f"{self.folder_prefix}/{file_name}"
                else:
                    return Response({"detail": "Failed to upload file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProductSerializer(product, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                print("Serializer errors:", serializer.errors)
                return Response({'message': 'Upload failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
