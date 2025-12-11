#importiere die nötigen Module
from flask import render_template, request, session
from flask_bcrypt import Bcrypt
from datetime import timedelta
from . import admin_register_data_require_blueprint, register_admin_blueprint

#Importiere die Datenbankklasse
from data.admin_database import DatabaseAdmin

#Importiere Hilfsfunktionen
from utils.uuid_generator import generate_uuid

#Importiere das Formular
from forms.Register_Admin_Form import RegisterForm

#Importiere den EMail Service und Code Generator
from utils.EMail import EmailService
from utils.codeGenerator import CodeGenerator
from utils.get_datetime import get_current_datetime_aware_utc
from utils.trackIP import whitlist_ips, allowed_ips

bcrypt = Bcrypt()
db = DatabaseAdmin("admin")

#Erstellt die Verbindung zur HTML Datei her
@register_admin_blueprint.route('/', methods=['GET', 'POST'])
@whitlist_ips(allowed_ips)
def index():
    form = RegisterForm()
    return render_template('register_admin.html',
                           form=form)

@admin_register_data_require_blueprint.route('/require', methods=['POST'])
def register_require():
    data = request.get_json()
    if not data:
        return {"status": "error", "message": "Ungültige Anfrage."}, 400
    
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    if db.find_admin_by_email(email):
        return {"status": "error", "message": "E-Mail-Adresse ist bereits registriert."}, 400
    
    verify_code = CodeGenerator.generate_verification_code()
    uuid_user = generate_uuid()
    session['admin_uuid'] = uuid_user
    
    user_data = db.admin_formular(
            uuid=uuid_user,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            code=verify_code,
            expiresAt=get_current_datetime_aware_utc() + timedelta(minutes=10)
        )

    EmailService.send_verify_email(email, verify_code)

    db.create_admin(user_data)
    return {"status": "success", "message": "Dein Konto wurde erfolgreich erstellt! Verifiziere dein Konto und Melde dich an!"}, 200