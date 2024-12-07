import hashlib
from flask import Blueprint, request

# Importar modelos
from app.models.client import Client
from app.models.product import Product
from app.models.service import Service

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/clientes', methods=['POST'])
def create_new_client():
    data = request.get_json()

    new_client = Client(
        id_client=None,
        name=data['name'],
        last_name_pat=data['last_name_pat'],
        last_name_mat=data['last_name_mat'],
        phone=data['phone'],
        email=data['email'],
        password=data['password'],
    )

    # Encriptar la contraseña
    new_client.password = hashlib.sha256(new_client.password.encode()).hexdigest()

    # Ejecutar el procedimiento almacenado
    response = new_client.execute(1)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Cliente creado correctamente" }

@api_bp.route('/api/clientes/<int:id>', methods=['PUT'])
def update_client(id):
    data = request.get_json()
    old_password = data['old_password']

    client = Client(
        id_client=id,
        name=data['name'],
        last_name_pat=data['last_name_pat'],
        last_name_mat=data['last_name_mat'],
        phone=data['phone'],
        email=data['email'],
        password=data['password'],
    )

    if old_password != client.password: 
        client.password = hashlib.sha256(client.password.encode()).hexdigest()

    # Ejecutar el procedimiento almacenado
    response = client.execute(3)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Cliente actualizado correctamente" }

@api_bp.route('/api/clientes/<int:id>', methods=['DELETE'])
def delete_client(id):
    client = Client(id_client=id)

    # Ejecutar el procedimiento almacenado
    response = client.execute(2)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Cliente eliminado correctamente" }





@api_bp.route('/api/productos', methods=['POST'])
def create_new_product():
    data = request.get_json()

    new_product = Product(
        id_product=None,
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
    )

    # Ejecutar el procedimiento almacenado
    response = new_product.execute(1)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Producto creado correctamente" }

@api_bp.route('/api/productos/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()

    product = Product(
        id_product=id,
        name=data['name'],
        description=data['description'],
        price=data['price'],
        stock=data['stock'],
    )

    # Ejecutar el procedimiento almacenado
    response = product.execute(3)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Producto actualizado correctamente" }

@api_bp.route('/api/productos/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product(id_product=id)

    # Ejecutar el procedimiento almacenado
    response = product.execute(2)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Producto eliminado correctamente" }





@api_bp.route('/api/servicios', methods=['POST'])
def create_new_service():
    data = request.get_json()

    new_service = Service(
        id_service=None,
        name=data['name'],
        description=data['description'],
        price=data['price'],
    )

    # Ejecutar el procedimiento almacenado
    response = new_service.execute(1)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Servicio creado correctamente" }

@api_bp.route('/api/servicios/<int:id>', methods=['PUT'])
def update_service(id):
    data = request.get_json()

    service = Service(
        id_service=id,
        name=data['name'],
        description=data['description'],
        price=data['price'],
    )

    # Ejecutar el procedimiento almacenado
    response = service.execute(3)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Servicio actualizado correctamente" }

@api_bp.route('/api/servicios/<int:id>', methods=['DELETE'])
def delete_service(id):
    service = Service(id_service=id)

    # Ejecutar el procedimiento almacenado
    response = service.execute(2)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    return { "message": "Servicio eliminado correctamente" }
