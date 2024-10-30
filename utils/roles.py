# Vou manter aqui por todas as views ta importando ele kkkk quando eu atualizar todas eu retiro
# produtos 

# ainda não decidi o list e o retrieve se vai ser aberto a todos ou se crio algumas exceções especificas
PRODUCTS_ROLES = {
    'list': [],
    'list_total': ['atendente_loja', 'superuser', 'estagiario'],
    'retrieve': [],
    'partial_update' : ['atendente_loja', 'superuser'],
    'create': ['atendente_loja', 'superuser'],
    'update': ['atendente_loja', 'superuser'],
    'destroy': ['atendente_loja', 'superuser']
}

class BanhotosaRoles: #OK
    APPOINTMENT_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_banhotosa', 'superuser', 'estagiario'],
        'partial_update': ['atendente_banhotosa', 'superuser'],
        'create': ['atendente_banhotosa', 'superuser'],
        'update': ['atendente_banhotosa', 'superuser'],
        'destroy': ['atendente_banhotosa', 'superuser']
    }

    SERVICETYPE_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': ['groomer', 'atendente_banhotosa', 'superuser'],
        'create': ['groomer', 'atendente_banhotosa', 'superuser'],
        'update': ['groomer', 'atendente_banhotosa', 'superuser'],
        'destroy': ['groomer', 'atendente_banhotosa', 'superuser']
    }

    PRODUCTUSED_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': ['groomer', 'atendente_banhotosa', 'superuser'],
        'create': ['groomer', 'atendente_banhotosa', 'superuser'],
        'update': ['groomer', 'atendente_banhotosa', 'superuser'],
        'destroy': ['groomer', 'atendente_banhotosa', 'superuser']
    }


class HotelRoles: #OK
    RESERVATION_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_hotel', 'superuser', 'estagiario'],
        'partial_update': ['atendente_hotel', 'superuser'],
        'create': ['atendente_hotel', 'superuser'],
        'update': ['atendente_hotel', 'superuser'],
        'destroy': ['atendente_hotel', 'superuser']
    }

    SERVICE_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': ['atendente_hotel', 'superuser'],
        'create': ['atendente_hotel', 'superuser'],
        'update': ['atendente_hotel', 'superuser'],
        'destroy': ['atendente_hotel', 'superuser']
    }

    RESERVATIONSERVICE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_hotel', 'superuser', 'estagiario'],
        'partial_update': ['atendente_hotel', 'superuser'],
        'create': ['atendente_hotel', 'superuser'],
        'update': ['atendente_hotel', 'superuser'],
        'destroy': ['atendente_hotel', 'superuser']
    }


class LojaRoles: #Ok
    SALE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_loja', 'superuser', 'estagiario'],
        'partial_update': ['atendente_loja', 'superuser'],
        'create': ['atendente_loja', 'superuser'],
        'update': ['atendente_loja', 'superuser'],
        'destroy': ['atendente_loja', 'superuser']
    }

    SALEPRODUCT_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_loja', 'superuser', 'estagiario'],
        'partial_update': ['atendente_loja', 'superuser'],
        'create': ['atendente_loja', 'superuser'],
        'update': ['atendente_loja', 'superuser'],
        'destroy': ['atendente_loja', 'superuser']
    }


class PetRoles: #OK
    SPECIE_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'create': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'update': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'destroy': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser']
    }

    BREED_ROLES = { 
        'list': [],
        'retrieve': [],
        'partial_update': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'create': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'update': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'destroy': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser']
    }

    PET_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'estagiario', 'superuser'],
        'partial_update': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'create': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'update': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser'],
        'destroy': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser']
    }


class ProdutosRoles: # OK
    PRODUCT_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['atendente_loja', 'superuser', 'estagiario'], # Este a lógica muda um pouco, neste caso é só um filtro da informação retornada diferentemente dos outros que relacionam o usuário com a informação pra verificar se o mesmo tem acesso.
        'partial_update': ['atendente_loja', 'superuser'],
        'create': ['atendente_loja', 'superuser'],
        'update': ['atendente_loja', 'superuser'],
        'destroy': ['atendente_loja', 'superuser']
    }


class SaudeRoles: #OK
    TREATMENTCYCLE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['medico_veterinario', 'atendente_saude', 'superuser', 'estagiario'],
        'partial_update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'create': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'destroy': ['medico_veterinario', 'atendente_saude', 'superuser']
    }

    SERVICE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['medico_veterinario', 'atendente_saude', 'superuser', 'estagiario'],
        'partial_update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'create': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'destroy': ['medico_veterinario', 'atendente_saude', 'superuser']
    }

    EXAMTYPE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['medico_veterinario', 'atendente_saude', 'superuser', 'estagiario'],
        'partial_update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'create': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'destroy': ['medico_veterinario', 'atendente_saude', 'superuser']
    }

    EXAM_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': ['medico_veterinario', 'atendente_saude', 'superuser', 'estagiario'],
        'partial_update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'create': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'update': ['medico_veterinario', 'atendente_saude', 'superuser'],
        'destroy': ['medico_veterinario', 'atendente_saude', 'superuser']
    }


class UsuariosRoles: #OK
    USER_ROLES = {
        'list': [],
        'list_total': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'estagiario', 'superuser'],
        'retrieve': [],
        'retrieve_total': ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'estagiario', 'superuser'],
        'partial_update': [],
        'partial_update_total': ['superuser'],
        'create': [],  # O create tem que ser publico mas so para o cargo user
        'create_total': ['superuser'],
        'update': [],
        'update_total': ['superuser'],
        'destroy': [],
        'destroy_total': ['superuser']
    }

    USERDOCUMENT_ROLES = {
        'list': [],
        'list_total': ['estagiario', 'superuser'],
        'retrieve': [],
        'retrieve_total': ['estagiario', 'superuser'],
        'partial_update': [],
        'partial_update_total': ['superuser'],
        'create': [],  # O create tem que ser publico mas so para o proprio usuário
        'create_total': ['superuser'],
        'update': [],
        'update_total': ['superuser'],
        'destroy': [],
        'destroy_total': ['superuser']
    }

    USERPHOTO_ROLES = {
        'list': [],
        'list_total': ['estagiario', 'superuser'],
        'retrieve': [],
        'retrieve_total': ['estagiario', 'superuser'],
        'partial_update': [],
        'partial_update_total': ['superuser'],
        'create': [],  # O create tem que ser publico mas so para o proprio usuário
        'create_total': ['superuser'],
        'update': [],
        'update_total': ['superuser'],
        'destroy': [],
        'destroy_total': ['superuser']
    }

    USERAUDIO_ROLES = {
        'list': [],
        'list_total': ['estagiario', 'superuser'],
        'retrieve': [],
        'retrieve_total': ['estagiario', 'superuser'],
        'partial_update': [],
        'partial_update_total': ['superuser'],
        'create': [],  # O create tem que ser publico mas so para o proprio usuário
        'create_total': ['superuser'],
        'update': [],
        'update_total': ['superuser'],
        'destroy': [],
        'destroy_total': ['superuser']
    }
