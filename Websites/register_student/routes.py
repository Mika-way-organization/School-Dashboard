#importiere die nötigen Module
from flask import render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from datetime import timedelta
from . import register_student_blueprint

#Importiere die Datenbankklasse
from data.database import DatabaseStudent

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
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Überprüft, ob die E-Mail-Adresse bereits registriert ist
        if db.find_student_by_email(form.email.data):
            flash('E-Mail-Adresse ist bereits registriert.', 'danger')
            print("E-Mail-Adresse ist bereits registriert.")
            return redirect(url_for('register_student.index'))
        
        verify_code = CodeGenerator.generate_verification_code()
        uuid = generate_uuid()
        
        # Erstellt die Benutzerdaten
        user_data = db.student_formular(
            uuid=uuid,
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,
            school_name=form.selectfield.data,
            code=verify_code,
            expiresAt=get_current_datetime_aware_utc() + timedelta(minutes=10)
        )

        EmailService.send_verify_email(form.email.data, verify_code)

        db.create_student(user_data)
        flash('Dein Konto wurde erfolgreich erstellt! Verifiziere dein Konto und Melde dich an!', 'success')
        print("Neuer Student erfolgreich registriert.")
        return redirect(url_for('codeconfirm.index', uuid=uuid))
    
    return render_template('register_student.html', 
                           form=form)