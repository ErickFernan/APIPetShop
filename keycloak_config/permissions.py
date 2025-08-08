from rest_framework import permissions

class HasRolePermission(permissions.BasePermission):
    """
    Função para verificar se o token relacioado ao usuário possui permissão
    para acessar alguma recurso.
    """
    def has_permission(self, request, view):
        roles_required = getattr(view, 'roles_required', None)

        if roles_required is None:
            return True

        user_roles = getattr(request, 'roles', [])

        for action, roles in roles_required.items():
            if view.action == action:
                if roles == []:
                    return True
                for role in roles:
                    if role in user_roles:
                        return True

        return False
