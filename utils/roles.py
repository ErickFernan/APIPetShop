PRODUCTS_ROLES = {
    'list': [],
    'retrieve': [],
    'partial_update' : ['atendente_loja', 'superuser'],
    'create': ['atendente_loja', 'superuser'],
    'update': ['atendente_loja', 'superuser'],
    'destroy': ['atendente_loja', 'superuser']
}
# Entretanto no produtos-basic eu preciso filtrar o retorno, ou seja, n posso enviar campos como photo_path, 
# storage_location, purchase_date, purchase_price, created_at, updated_at
 