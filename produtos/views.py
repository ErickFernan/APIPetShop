from django.shortcuts import get_object_or_404
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response

from produtos.models import Product
from produtos.serializers import ProductSerializer, ProductSerializerLimited
from produtos.filters import ProductFilter

from bucket.minio_client import delete_file

from utils.validations import image_validation, validate_serializer_and_upload_file
from utils.functions import extract_file_details
from utils.views import BaseViewSet
from utils.roles import ProdutosRoles
from utils.exceptions import manage_exceptions


class ProductViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    roles_required = ProdutosRoles.PRODUCT_ROLES

    folder_prefix = 'products'

    def create(self, request):
        try:
            data = request.data
            file = request.FILES.get('photo')
            file_name, content_type = None, None

            if file:
                image_validation(file=file)

                file_name, content_type = extract_file_details(file)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
        
        except Exception as e:
            return manage_exceptions(e, context='create')
    
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                product = get_object_or_404(self.queryset, id=pk)

                if product.photo_path:
                    delete_success, e = delete_file(product.photo_path)
                    if not delete_success:
                        raise Exception(e)

                product.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

    def update(self, request, *args, **kwargs):  
        try:
            pk = kwargs.get('pk')
            product = get_object_or_404(self.queryset, id=pk)

            data = request.data
            file = request.FILES.get('photo')
            file_name, content_type = product.photo_path.split('/')[-1] if product.photo_path else None, None
             
            if file:
                is_valid, message = image_validation(file=file)
            
                file_name, content_type = extract_file_details(file, product)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(product, data=data)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
            
        except Exception as e:
            return manage_exceptions(e, context='update')
            
    def partial_update(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')
            product = get_object_or_404(self.queryset, id=pk)

            data = request.data
            file = request.FILES.get('photo')
            file_name, content_type = product.photo_path.split('/')[-1] if product.photo_path else None, None
             
            if file:
                is_valid, message = image_validation(file=file)
            
                file_name, content_type = extract_file_details(file, product)
                data['photo_path'] = f"{self.folder_prefix}/{file_name}"

            serializer = self.serializer_class(product, data=data, partial=True)

            return validate_serializer_and_upload_file(serializer, file, file_name, content_type, self.folder_prefix)
            
        except Exception as e:
            return manage_exceptions(e, context='partial_update')
            
    def list(self, request):
        try:
            list_products = self.filter_queryset(self.queryset)

            if any(role in self.roles_required['list_retrive_total'] for role in request.roles):
                list_serializer = self.serializer_class(list_products, many=True)
                return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

            list_serializer = ProductSerializerLimited(list_products, many=True)
            return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='list')

    def retrieve(self, request, *args, **kwargs):    
        try:
            pk = kwargs.get('pk')
            product = get_object_or_404(self.queryset, id=pk)

            if any(role in self.roles_required['list_retrive_total']  for role in request.roles):
                list_serializer = self.serializer_class(product)
                return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

            list_serializer = ProductSerializerLimited(product)
            return Response({'produtos': list_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')
