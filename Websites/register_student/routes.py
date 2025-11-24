#importiere die nötigen Module
from pymongo import MongoClient
from flask import render_template, request, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from . import register_student_blueprint

#Importiere die Datenbankklasse
from data.database import Database

#Importiere Hilfsfunktionen
from utils.uuid_generator import generate_uuid

#Importiere das Formular
from forms.Register_Form import RegisterForm

bcrypt = Bcrypt()
db = Database("student")

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
        
        # Erstellt die Benutzerdaten
        user_data = db.student_formular(
            uuid=generate_uuid(),
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,
            school_name=form.selectfield.data
        )

        db.create_student(user_data)
        flash('Dein Konto wurde erfolgreich erstellt! Du kannst dich jetzt anmelden.', 'success')
        print("Neuer Student erfolgreich registriert.")
        return redirect(url_for('login.index'))
    
    return render_template('register_student.html', 
                           form=form)