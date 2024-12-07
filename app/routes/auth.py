import hashlib
from flask import Blueprint, render_template, request, make_response
from app.models.client import Client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login')
def send_login_view():
    return render_template('login.html')

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    client = Client(email=data["email"], password=hashlib.sha256(data["password"].encode()).hexdigest())
    response = client.execute(5)

    if response["valido"] != 1:
        return { "error": response["error"] }
    
    response = make_response({ "message": "Autenticación Existosa" })
    response.set_cookie("Authorization", client.email)

    return response
