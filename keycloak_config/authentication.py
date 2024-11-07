from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings

from keycloak_config.keycloak_client import keycloak_openid

from utils.logs_config import handle_exception


class KeyCloakAuthentication(authentication.BaseAuthentication):
    """
    Função com a lógica necessária para fazer a validação do token fornecido na
    requisição, utilizando a rota de introspecção do keycloak
    """
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')

        if not token or not token.startswith('Bearer '):
            raise AuthenticationFailed('No token provided or invalid token format')
        
        token = token.split(" ")[1]
        
        try:
            token_info = keycloak_openid.introspect(token)
            
            if not token_info.get('active'):
                raise AuthenticationFailed('Token is invalid')

            # Extrair informações do token (personalizar conforme a necessidade)
            current_user = token_info.get('preferred_username')
            currente_user_id = token_info.get('django_uuid') # Aqui ele pega carrega o id do proprio usuário no django
            roles = token_info.get('realm_access', {}).get('roles', [])
            
            # Adicionar informações ao request para acesso nas views
            request.current_user = current_user
            request.current_user_id = currente_user_id
            request.roles = roles

            return current_user, roles

        except Exception as e:
            handle_exception('authenticate', e)
