#importiere die nötigen Module
from flask import render_template, request, redirect, url_for, session
from flask_login import current_user
from flask_bcrypt import Bcrypt
from datetime import timedelta
from . import register_student_blueprint, register_data_require_blueprint

#Importiere die Datenbankklasse
from data.student_database import DatabaseStudent

#Importiere Hilfsfunktionen
from utils.uuid_generator import generate_uuid

#Importiere das Formular
from forms.Register_Form import RegisterForm

#Importiere den EMail Service und Code Generator
from utils.EMail import EmailService
from utils.codeGenerator import CodeGenerator
from utils.get_datetime import get_current_datetime_aware_utc

bcrypt = Bcrypt()
db = DatabaseStudent("student")

#Erstellt die Verbindung zur HTML Datei her
@register_student_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = RegisterForm()
    return render_template('register_student.html',
                           form=form)

@register_data_require_blueprint.route('/require', methods=['POST'])
def register_require():
    data = request.get_json()
    if not data:
        return {"status": "error", "message": "Ungültige Anfrage."}, 400
    
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    # Wird noch bearbeitet
    #school_name = data.get('school_name')
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    if db.find_student_by_email(email):
        return {"status": "error", "message": "E-Mail-Adresse ist bereits registriert."}, 400
    
    verify_code = CodeGenerator.generate_verification_code()
    uuid = generate_uuid()
    session['uuid'] = uuid
    
    user_data = db.student_formular(
        uuid=uuid,
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        school_id=None,
        code=verify_code,
        expiresAt=get_current_datetime_aware_utc() + timedelta(minutes=10)
    )

    EmailService.send_verify_email(email, verify_code)

    db.create_student(user_data)
    return {"status": "success", "message": "Dein Konto wurde erfolgreich erstellt! Verifiziere dein Konto und Melde dich an!"}, 200