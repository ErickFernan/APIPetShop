from keycloak import KeycloakOpenID
from django.conf import settings


keycloak_openid = KeycloakOpenID(
    server_url=settings.DJ_KC_SERVER_URL,
    client_id=settings.DJ_KC_CLIENT_ID,
    realm_name=settings.DJ_KC_REALM ,
    client_secret_key=settings.DJ_KC_CLIENT_SECRET
)
