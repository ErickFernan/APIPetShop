import requests

from keycloak import KeycloakOpenID, KeycloakAdmin, KeycloakOpenIDConnection

from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from utils.logs_config import handle_exception, log_exception
from utils.exceptions import manage_exceptions


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
    client_id=settings.DJ_KC_CLIENT_PUBLIC_ID,
    verify=True
)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

def get_role_info(role_name):
    try:
        role = keycloak_admin.get_realm_role(role_name)
        return role
    except Exception as e:
        handle_exception('get_role_info', e)

def get_user_info(username):
    try:
        return keycloak_admin.get_user_id(username)
    except Exception as e:
        handle_exception('get_user_info', e)

def get_user_info2(username): # renomear
    try:
        return keycloak_admin.get_user(username)
    except Exception as e:
        handle_exception('get_user_info2', e)

def assign_role_to_user(user_id, role):
    try:
        keycloak_admin.assign_realm_roles(user_id=user_id, roles=[role])
    except Exception as e:
        handle_exception('assign_role_to_user', e)

def set_password(user_id, password):
    try:
        keycloak_admin.set_user_password(user_id=user_id, password=password, temporary=False)
    except Exception as e:
        handle_exception('set_password', e)

def add_user_to_auth_service(username, email, firstName, lastName):
    try:
        user_id_keycloak = keycloak_admin.create_user({
            "username": username,
            "email": email,
            "enabled": True,
            "firstName": firstName,
            "lastName": lastName,
            "attributes": {
                "locale": ["pt-BR"]
            }
        }, exist_ok=False)
        return user_id_keycloak
    except Exception as e:
        handle_exception('add_user_to_auth_service', e)

def delete_user_to_auth_service(user_auth_id):
    try:
        keycloak_admin.delete_user(user_auth_id)
    except Exception as e:
        handle_exception('delete_user_to_auth_service', e)

def update_user_to_auth_service(user_id, payload):
    try:
        keycloak_admin.update_user(user_id, payload)
    except Exception as e:
        handle_exception('update_user_to_auth_service', e) 

def send_email_update_password(user_id):
    try:
        token = keycloak_connection.token

        url = f"{settings.DJ_KC_SERVER_URL}/admin/realms/{settings.DJ_KC_REALM}/users/{user_id}/reset-password-email"
        headers = {
                "Authorization": f"Bearer {token['access_token']}"
            }
        
        response = requests.put(url, headers=headers, params={"client_id": "admin-rest-client"})
        
        if response.status_code == 204:
            return Response({'message': "Um erro ocorreu na exclusão do seu usuario, um email de att de senha foi enviado. pfvr redefina sua senha."}, status=status.HTTP_400_BAD_REQUEST)
            print("E-mail para resetar a senha enviado com sucesso!")
        else:
            print(f"Erro ao enviar e-mail: {response.text}")
    
    except Exception as e:
        log_exception('send_email_update_password', e)
        

def rollback_update_keycloak(user_auth_service_id, user):
    """
    Função para realizar o rollback no Keycloak em caso de falha na operação principal.
    Neste caso ele retorna as pro estado original as informações que foram modificadas

    Args:
        user_auth_service_id (str): ID do usuário no Keycloak.
        user (User): Instância do usuário para recuperar os dados de email, nome e sobrenome.

    Returns:
        Response ou None: Retorna uma resposta de erro caso o rollback falhe.
    """
    try:
        update_user_to_auth_service(
            user_id=user_auth_service_id,
            payload={
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name
            }
        )
    except Exception as e:
        log_exception('update (rollback)', e)
        # handle_exception('update_user_to_auth_service', e)

def rollback_create_keycloak(user_auth_service_id):
    """
    Função para realizar o rollback no Keycloak em caso de falha na operação principal.
    Neste caso ele deleta o usuário se ocorrer um erro

    Args:
        user_auth_service_id (str): ID do usuário no Keycloak.

    Returns:
        Response ou None: Retorna uma resposta de erro caso o rollback falhe.
    """
    try:
        delete_user_to_auth_service(user_auth_service_id)
    except Exception as e:
        log_exception('create (rollback)', e)
        # handle_exception('update_user_to_auth_service', e)


def rollback_delete_keycloak(user, user_id):
    """
    Função para realizar o rollback no Keycloak em caso de falha na operação principal.
    Neste caso ele retorna as pro estado original as informações que foram modificadas

    Args:
        user_auth_service_id (str): ID do usuário no Keycloak.
        user (User): Instância do usuário para recuperar os dados de email, nome e sobrenome.

    Returns:
        Response ou None: Retorna uma resposta de erro caso o rollback falhe.
    """
    try:
        user_auth_service_id = add_user_to_auth_service(username=user.username, 
                                                        email=user.email, 
                                                        firstName=user.first_name, 
                                                        lastName=user.last_name)

        user.auth_service_id = user_auth_service_id
        user.id = user_id
        user.save()
        assign_role_to_user(user_auth_service_id, get_role_info(user.role))
        update_user_to_auth_service(user_id=get_user_info(username=user.username),
                                                payload={"email": user.email,
                                                         "firstName": user.first_name,
                                                         "lastName": user.last_name,
                                                         "attributes": {
                                                            "django_uuid": [str(user.id)]
                                                        }})

        keycloak_admin.set_user_password(user_id=user.auth_service_id, password='password', temporary=True)                                               
        
        response = send_email_update_password(user_id=user_auth_service_id)
        print(f"E-mail de redefinição de senha enviado para {user.username}.")
        return response

    except Exception as e:
        log_exception('delete (rollback)', e)
