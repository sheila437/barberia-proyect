from flask import Blueprint, render_template, request, redirect, url_for
import app.database.connect as database
# Importar modelos
from app.models.client import Client
from app.models.product import Product
from app.models.service import Service
from app.models.cite import Cite

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def is_admin():
    cookie = request.cookies.get('Authorization')
    if not cookie:
        return redirect(url_for('auth.login'))
    
    if cookie != 'admin@admin.com':
        return redirect("/")

@admin_bp.route('/admin')
def send_admin_view():
    return render_template('admin.html')

@admin_bp.route('/admin/citas')
def send_admin_citas_view():
    search = request.args.get('search')
    if search == "":
        search = None

    citeInstance = Cite(date=search)
    response = citeInstance.execute(1)
    cites = response["cites"]

    clientInstance = Client()
    response = clientInstance.execute(4)
    clients = response["clients"]

    serviceInstance = Service()
    response = serviceInstance.execute(4)
    services = response["services"]

    pendientes = len([cite for cite in cites if cite[3] == "pendiente"])
    realizadas = len([cite for cite in cites if cite[3] == "realizada"])
    canceladas = len([cite for cite in cites if cite[3] == "cancelada"])

    return render_template('admin_citas.html', services=services, clients=clients, cites=cites, search=search, pendientes=pendientes, realizadas=realizadas, canceladas=canceladas)

@admin_bp.route('/admin/citas/agregar', methods=['POST'])
def send_admin_citas_agregar():
    data = request.get_json()
    date = data.get('date')
    id_service = data.get('id_service')
    id_client = data.get('id_client')

    print(date, id_service, id_client)

    citeInstance = Cite(date=date, id_service=id_service, id_client=id_client)
    response = citeInstance.execute(2)

    if response["valido"] != 1:
        return { "error": response["error"] }

    return { "message": "Cita creada correctamente" }

@admin_bp.route('/admin/citas/actualizar', methods=['POST'])
def send_admin_citas_actualizar():
    data = request.get_json()
    option = data.get('option')
    id_cite = data.get('id')

    citeInstance = Cite(id_cite=id_cite)
    response = citeInstance.execute(option)

    if response["valido"] != 1:
        return { "error": response["error"] }

    return { "message": "Cita actualizada correctamente" }

@admin_bp.route('/admin/clientes')
def send_admin_clientes_view():
    search = request.args.get('search')
    clientInstance = Client(name=search)

    response = clientInstance.execute(4)
    clients = response["clients"]

    return render_template('admin_clientes.html', clients=clients)

@admin_bp.route('/admin/productos')
def send_admin_productos_view():
    search = request.args.get('search')
    productInstance = Product(name=search)

    response = productInstance.execute(4)
    products = response["products"]

    return render_template('admin_productos.html', products=products)

@admin_bp.route('/admin/servicios')
def send_admin_servicios_view():
    search = request.args.get('search')
    serviceInstance = Service(name=search)

    response = serviceInstance.execute(4)
    services = response["services"]

    return render_template('admin_servicios.html', services=services)

@admin_bp.route('/admin/citas_historial', methods=['GET'])
def send_admin_historial_citas_view():
    cursor = database.connection.cursor(dictionary=True)
    month = request.args.get('month')
    year = request.args.get('year')

    query = """
        SELECT 
            c.id_cita,
            c.fecha,
            c.asistencia,
            c.estado,
            s.nombre AS servicio,
            CONCAT(cl.nombre, ' ', cl.apellido_paterno, ' ', cl.apellido_materno) AS cliente,
            s.precio
        FROM CITAS c
        JOIN SERVICIOS s ON c.id_servicio = s.id_servicio
        JOIN CLIENTES cl ON c.id_clientes = cl.id_clientes
    """
    filters = []
    params = []

    if month:
        filters.append("MONTH(c.fecha) = %s")
        params.append(month)
    if year:
        filters.append("YEAR(c.fecha) = %s")
        params.append(year)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY c.fecha ASC"

    cursor.execute(query, params)
    citas = cursor.fetchall()

    total_precio = sum(cita['precio'] for cita in citas)
    return render_template('admin_historial_citas.html', 
        citas=citas, 
        month=month, 
        year=year, 
        total_precio=total_precio
    )
