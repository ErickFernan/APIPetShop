class RolesUtils:
    BANHOTOSA_COMMON_ROLES = ['atendente_banhotosa', 'superuser']
    BANHOTOSA_GROOMER_ROLES = ['groomer'] + BANHOTOSA_COMMON_ROLES
    HOTEL_COMMON_ROLES = ['atendente_hotel', 'superuser']
    LOJA_COMMON_ROLES = ['atendente_loja', 'superuser']
    PET_COMMON_ROLES = ['atendente_saude', 'atendente_hotel', 'atendente_loja', 'atendente_banhotosa', 'superuser']
    PRODUTO_COMMON_ROLES = LOJA_COMMON_ROLES
    SAUDE_COMMON_ROLES = ['medico_veterinario', 'atendente_saude', 'superuser']
    USER_COMMON_ROLES = PET_COMMON_ROLES
    
    @staticmethod
    def get_roles(base_roles, additional_roles=None):
        return base_roles if not additional_roles else base_roles + additional_roles


class BanhotosaRoles: # Adicionar doc string
    APPOINTMENT_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': RolesUtils.get_roles(RolesUtils.BANHOTOSA_COMMON_ROLES, ['estagiario']),
        'partial_update': RolesUtils.BANHOTOSA_COMMON_ROLES,
        'create': RolesUtils.BANHOTOSA_COMMON_ROLES,
        'update': RolesUtils.BANHOTOSA_COMMON_ROLES,
        'destroy': RolesUtils.BANHOTOSA_COMMON_ROLES,
    }
    SERVICETYPE_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': RolesUtils.BANHOTOSA_GROOMER_ROLES,
        'create': RolesUtils.BANHOTOSA_GROOMER_ROLES,
        'update': RolesUtils.BANHOTOSA_GROOMER_ROLES,
        'destroy': RolesUtils.BANHOTOSA_GROOMER_ROLES,
    }
    APPOINTMENTSERVICE_ROLES = SERVICETYPE_ROLES # Como modiquei depois, averiguar se está correto e eu nbão  preciso do campo list_retrieve_total
    PRODUCTUSED_ROLES = SERVICETYPE_ROLES


class HotelRoles:
    RESERVATION_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': RolesUtils.get_roles(RolesUtils.HOTEL_COMMON_ROLES, ['estagiario']),
        'partial_update': RolesUtils.HOTEL_COMMON_ROLES,
        'create': RolesUtils.HOTEL_COMMON_ROLES,
        'update': RolesUtils.HOTEL_COMMON_ROLES,
        'destroy': RolesUtils.HOTEL_COMMON_ROLES,
    }
    SERVICE_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': RolesUtils.HOTEL_COMMON_ROLES,
        'create': RolesUtils.HOTEL_COMMON_ROLES,
        'update': RolesUtils.HOTEL_COMMON_ROLES,
        'destroy': RolesUtils.HOTEL_COMMON_ROLES,
    }
    RESERVATIONSERVICE_ROLES = RESERVATION_ROLES


class LojaRoles:
    SALE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': RolesUtils.get_roles(RolesUtils.LOJA_COMMON_ROLES, ['estagiario']),
        'partial_update': RolesUtils.LOJA_COMMON_ROLES,
        'create': RolesUtils.LOJA_COMMON_ROLES,
        'update': RolesUtils.LOJA_COMMON_ROLES,
        'destroy': RolesUtils.LOJA_COMMON_ROLES,
    }
    SALEPRODUCT_ROLES = SALE_ROLES


class PetRoles:
    SPECIE_ROLES = {
        'list': [],
        'retrieve': [],
        'partial_update': RolesUtils.PET_COMMON_ROLES,
        'create': RolesUtils.PET_COMMON_ROLES,
        'update': RolesUtils.PET_COMMON_ROLES,
        'destroy': RolesUtils.PET_COMMON_ROLES,
    }
    BREED_ROLES = SPECIE_ROLES
    PET_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': RolesUtils.get_roles(RolesUtils.PET_COMMON_ROLES, ['estagiario']),
        'partial_update': RolesUtils.PET_COMMON_ROLES,
        'create': RolesUtils.PET_COMMON_ROLES,
        'update': RolesUtils.PET_COMMON_ROLES,
        'destroy': RolesUtils.PET_COMMON_ROLES,
    }


class ProdutosRoles:
    PRODUCT_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': RolesUtils.get_roles(RolesUtils.PRODUTO_COMMON_ROLES, ['estagiario']), # Este a lógica muda um pouco, neste caso é só um filtro da informação retornada, diferentemente dos outros que relacionam o usuário com a informação pra verificar se o mesmo tem acesso.
        'partial_update': RolesUtils.PRODUTO_COMMON_ROLES,
        'create': RolesUtils.PRODUTO_COMMON_ROLES,
        'update': RolesUtils.PRODUTO_COMMON_ROLES,
        'destroy': RolesUtils.PRODUTO_COMMON_ROLES,
    }


class SaudeRoles:
    TREATMENTCYCLE_ROLES = {
        'list': [],
        'retrieve': [],
        'list_retrive_total': RolesUtils.get_roles(RolesUtils.SAUDE_COMMON_ROLES, ['estagiario']),
        'partial_update': RolesUtils.SAUDE_COMMON_ROLES,
        'create': RolesUtils.SAUDE_COMMON_ROLES,
        'update': RolesUtils.SAUDE_COMMON_ROLES,
        'destroy': RolesUtils.SAUDE_COMMON_ROLES,
    }
    SERVICE_ROLES = TREATMENTCYCLE_ROLES
    EXAMTYPE_ROLES = TREATMENTCYCLE_ROLES
    EXAM_ROLES = TREATMENTCYCLE_ROLES


class UsuariosRoles:
    USER_ROLES = {
        'list': [],
        'list_total': RolesUtils.get_roles(RolesUtils.USER_COMMON_ROLES, ['estagiario']),
        'retrieve': [],
        'retrieve_total': RolesUtils.get_roles(RolesUtils.USER_COMMON_ROLES, ['estagiario']), # Acho que aqui eu deveria mudar pra list_retrieve_total, depois conferir
        'partial_update': [],
        'partial_update_total': ['superuser'],
        'create': [], # O create tem que ser publico mas so para o cargo user
        'create_total': ['superuser'],
        'update': [],
        'update_total': ['superuser'],
        'destroy': [],
        'destroy_total': ['superuser'],
        'update_password': [],
        'update_password_total': ['superuser']
    }
    USERDOCUMENT_ROLES = USER_ROLES
    USERPHOTO_ROLES = USER_ROLES
    USERAUDIO_ROLES = USER_ROLES
