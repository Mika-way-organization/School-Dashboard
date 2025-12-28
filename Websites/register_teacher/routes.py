"""Weitere Überlegung

Der Lehrer kann sich nur registrieren, wenn er eine endweder per email oder eigenes Fomrular den Code erhalten hat.
Ist noch in bearbeitung.
"""


#importiere die nötigen Module
from flask import render_template, request, redirect, url_for, session
from flask_login import current_user
from flask_bcrypt import Bcrypt
from datetime import timedelta
from . import register_teacher_blueprint, register_teacher_data_require_blueprint

#Importiere die Datenbankklasse
from data.teacher_database import DatabaseTeacher

#Importiere Hilfsfunktionen
from utils.uuid_generator import generate_uuid

#Importiere das Formular
from forms.Register_Form_teacher import RegisterForm

#Importiere den EMail Service und Code Generator
from utils.EMail import EmailService
from utils.codeGenerator import CodeGenerator
from utils.get_datetime import get_current_datetime_aware_utc

bcrypt = Bcrypt()
db = DatabaseTeacher("teacher")

#Erstellt die Verbindung zur HTML Datei her
@register_teacher_blueprint.route('/<string:code>', methods=['GET', 'POST'])
def index(code):
    if code != "TEACHER2024": #Ein Beispielcode, der zur Registrierung berechtigt
        return redirect(url_for('page_not_found.index'))
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = RegisterForm()
    return render_template('register_teacher.html',
                           form=form)

@register_teacher_data_require_blueprint.route('/require/<string:code>', methods=['POST'])
def register_require(code):
    if code != "TEACHER2024": #Ein Beispielcode, der zur Registrierung berechtigt
        return {"status": "error", "message": "Ungültiger Registrierungscode."}, 400
    
    data = request.get_json()
    if not data:
        return {"status": "error", "message": "Ungültige Anfrage."}, 400
    
    username = data.get('username')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    password = data.get('password')
    #school_name = data.get('school_name') wird in Zukunft noch bearbeitet
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    if db.find_teacher_by_email(email):
        return {"status": "error", "message": "E-Mail-Adresse ist bereits registriert."}, 400
    
    verify_code = CodeGenerator.generate_verification_code()
    uuid_teacher = generate_uuid()
    session['teacher_uuid'] = uuid_teacher
    
    user_data = db.teacher_formular(
        uuid=uuid_teacher,
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        school_uuid=None,  # Wird in Zukunft noch bearbeitet
        code=verify_code,
        expiresAt=get_current_datetime_aware_utc() + timedelta(minutes=10)
    )

    EmailService.send_verify_email(email, verify_code)

    db.create_teacher(user_data)
    return {"status": "success", "message": "Dein Konto wurde erfolgreich erstellt! Verifiziere dein Konto und Melde dich an!"}, 200