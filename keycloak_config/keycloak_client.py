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

def assign_role_to_user(user_id, role_name):
    try:
        role = keycloak_admin.get_realm_role(role_name)
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