from utils.views import BaseViewSet
from utils.roles import LojaRoles
from utils.functions import has_permission, validate_required_fields
from utils.validations import validate_serializer_and_upload_file
from utils.exceptions import manage_exceptions

from rest_framework import status
from rest_framework.response import Response

from loja.models import Sale, SaleProduct
from loja.serializers import SaleSerializer, SaleCreateSerializer, SaleProductSerializer
from loja.filters import SaleFilter

from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from django_filters.rest_framework import DjangoFilterBackend



class SaleViewSet(BaseViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = SaleFilter
    
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    roles_required = LojaRoles.SALE_ROLES

    def create(self, request):
        """
            Por enquanto eu vou deixar essa observação pois pretendo escrever sobre.
            Os códigos comentados tinham a intenção de permitir a criação de vendas enviando um seller_id na requisição, 
            isso serviria, pois os usários criados junto com o keycloak não possuem um id na api, apesar de eles possuirem os grupos que
            dão privilegios para executar determinadas ações.
            desta forma se eu estou usando meu token de superuser(admin) eu conseguiria criar a venda com o seller_id que eu quisesse.
            mas esta opção abriu sérios problemas de segurança, como perca de responsabilidade individual, pois a forma que a função 
            verifica se o usuário possui permissão passaria a permitir que um um vendedor cadastrasse vendas com o id de outro vendendor
            e mais grave ainda, que usasse id de usuários comuns no seller id para salvar vendas.
            desta forma, refiz de forma que o seller_id seja sempre pego do token de quem está fazendo a requisição.
            assim não é possível fruadar quem fez a venda.
            quanto ao token do admin que é criado junto com o keycloak, ele passar a não conseguir criar uma sale
            mas para resolver isso basta criar um usuário pela api que seja superuser, desta forma ele vai ter acesso ao recurso.
            por outro lado, o seller id será salvo com o do super user, desta forma o mesmo precisará mudar manualmente para o seller_id correto
            Dado que a intenção é que apenas o atendente da loja faça o cadastro de vendas e o superuser seja usado apenas em caso de emergencia
            vou manter essa solução
            entretanto, futuramente, é interessante fazer uma melhoria desta lógica, uma vez que a lógica atual não trará problemas em uma 
            aplicação de empresa pequena, mas em caso de algo com uma estrutura maior, pode fazer falta. 
            Além da melhoria trazer conforto e facilidade no uso. 
        """
        try:
            data = request.data.copy()
            
            # if not data.get('seller_id') or not str(data.get('seller_id')).strip():
            #     data['seller_id'] = request.current_user_id or None # O None é para o caso dos usuário criado no up do keycloak e que não possuem o current_user_id. Ai nesse caso o seller_id vai ser obrigatório
            #     print(data['seller_id'])
        
            data['seller_id'] = request.current_user_id

            # extra_required_fields = ['seller_id', 'purchase_id']
            extra_required_fields = ['purchase_id']
            errors = validate_required_fields(data, extra_required_fields)
            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            
            if not has_permission(pk=data['seller_id'], request=request, roles=self.roles_required['create']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            serializer = SaleCreateSerializer(data=data)

            return validate_serializer_and_upload_file(serializer=serializer)
        
        except Exception as e:
            return manage_exceptions(e, context='create')
    
    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Update not allowed for Sale.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Partial Update not allowed for Sale.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                pk = kwargs.get('pk')
                sale = get_object_or_404(self.get_queryset(), id=pk)

                sale.delete()

                return Response({'message': 'Deleted successful!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='destroy')

    def list(self, request, *args, **kwargs):
        try:
            if any(role in self.roles_required['list_retrive_total'] for role in request.roles):
                list_sales = self.filter_queryset(self.get_queryset()) # preciso fazer o filtro para filtrar por nome tb
                # list_sales = self.get_queryset()  # Sem o filtro, retorna tudo
                list_serializer = self.serializer_class(list_sales, many=True)
                return Response({'usuários': list_serializer.data}, status=status.HTTP_200_OK)

            else:
                list_sales = get_list_or_404(self.get_queryset(), purchase_id=request.current_user_id) # Esse caso vai ser chamado apenas se não for alguns dos usuários com acesso total, ou seja, se não for um superuser, estágiario ou atendente loja, dessa forma vai buscar pelo comprador(purchase)
                list_serializer = self.serializer_class(list_sales, many=True)
                return Response({'usuário': list_serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return manage_exceptions(e, context='list')
        
    def retrieve(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk')       
            purchase_id = self.get_queryset().filter(pk=pk).values_list('purchase_id', flat=True).first() # so carrega o campo desejado

            if not has_permission(pk=str(purchase_id), request=request, roles=self.roles_required['list_retrive_total']):
                return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

            if not purchase_id:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

            pet = self.get_queryset().get(pk=pk)  # recupera o objeto completo
            pet_serializer = self.serializer_class(pet)
            return Response({'usuário': pet_serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return manage_exceptions(e, context='retrieve')


class SaleProductViewSet(BaseViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer
    roles_required = LojaRoles.SALEPRODUCT_ROLES
