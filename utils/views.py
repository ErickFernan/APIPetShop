from rest_framework import viewsets
from keycloak_config.authentication import KeyCloakAuthentication
from keycloak_config.permissions import HasRolePermission

class BaseViewSet(viewsets.ModelViewSet):
    """Se quiser testar sem a necessidade de token, basta comentar as duas linhas abaixo:"""
    authentication_classes = [KeyCloakAuthentication]
    permission_classes = [HasRolePermission]
    ...
   