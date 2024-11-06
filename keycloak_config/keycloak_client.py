"""
Eu optei por criar funções com as chamadas do python-keycloak, pois se o método mudar ou for utilizar um outro serviço no lugar do keycloak
vai ser necessário mudar apenas a regra dentro da função e não todo os codigos nas views por exemplo
"""
from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakOpenIDConnection

from django.conf import settings


keycloak_openid = KeycloakOpenID(
    server_url=settings.DJ_KC_SERVER_URL,
    client_id=settings.DJ_KC_CLIENT_ID,
    realm_name=settings.DJ_KC_REALM,
    client_secret_key=settings.DJ_KC_CLIENT_SECRET
)

keycloak_connection = KeycloakOpenIDConnection(
                        server_url=settings.DJ_KC_SERVER_URL,
                        username=settings.DJ_KC_ADMIN,
                        password=settings.DJ_KC_ADMIN_PASSWORD,
                        realm_name=settings.DJ_KC_REALM,
                        # user_realm_name=settings.DJ_KC_REALM, # Se o usuário administrador estiver em um realm personalizado (ou seja, fora do master), essa configuração deve ser especificada para garantir que o KeycloakAdmin se autentique corretamente.
                        client_id=settings.DJ_KC_CLIENT_PUBLIC_ID,
                        # client_secret_key=settings.DJ_KC_CLIENT_SECRET,
                        verify=True)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

def get_role_info(role_name):
    try:
        role = keycloak_admin.get_realm_role(role_name)
        return role

    except Exception as e:
        print(f"Erro: {e}")
        raise e

def get_user_info(username):
    return keycloak_admin.get_user_id(username)

def get_user_info2(username):
    return keycloak_admin.get_user(username)

def assign_role_to_user(user_id, role):
    try:
        keycloak_admin.assign_realm_roles(user_id=user_id, roles=[role])

    except Exception as e:
        print(f"Erro: {e}")
        raise e

def set_password(user_id, password):
    try:
        role = keycloak_admin.set_user_password(user_id=user_id, password=password, temporary=False)

    except Exception as e:
        print(f"Erro: {e}")
        raise e

def add_user_to_auth_service(username, email, firstName, lastName):
    user_id_keycloak = keycloak_admin.create_user({
                        "username": username,
                        "email": email,
                        "enabled": True,
                        "firstName": firstName,
                        "lastName": lastName,
                        "attributes": {
                            "locale": ["pt-BR"]
                        }
                    },
                    exist_ok=False)
    
    return user_id_keycloak

def delete_user_to_auth_service(user_auth_id):
    keycloak_admin.delete_user(user_auth_id)

def update_user_to_auth_service(user_id, payload):
    keycloak_admin.update_user(user_id, payload)