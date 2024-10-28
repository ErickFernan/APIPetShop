from django.shortcuts import get_object_or_404
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response

from produtos.models import Product
from produtos.serializers import ProductSerializer, ProductSerializerLimited
from produtos.filters import ProductFilter

from bucket.minio_client import upload_file, delete_file

from utils.validations import image_validation
from utils.functions import change_file_name
from utils.views import BaseViewSet
from utils.roles import PRODUCTS_ROLES


class ProductViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    roles_required = PRODUCTS_ROLES

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
                    return Response({"detail": "Failed to upload file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Upload successful!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print("Serializer errors:", serializer.errors)
                return Response({'message': 'Upload failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
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
                    return Response({"detail": "Failed to update file to MinIO"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.serializer_class(product, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Update successful!', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                print("Serializer errors:", serializer.errors)
                return Response({'message': 'Update failed!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def list(self, request):
        try:
            list_products = self.filter_queryset(self.queryset)

            if any(role in ['atendente_loja', 'superuser'] for role in request.roles):
                list_serializer = self.serializer_class(list_products, many=True)
                return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

            list_serializer = ProductSerializerLimited(list_products, many=True)
            return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            product = self.queryset.get(id=pk)

            if any(role in ['atendente_loja', 'superuser'] for role in request.roles):
                list_serializer = self.serializer_class(product)
                return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

            list_serializer = ProductSerializerLimited(product)
            return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            print("An unexpected error occurred:", e)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            