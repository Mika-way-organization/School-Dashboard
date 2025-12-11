"""Login Page

Wichtige Sache zum Login Bereich.

Es gibt nur diese Sessions:
- session['logged_in'] : Bool ob der User eingeloggt ist
- session['user_uuid'] : UUID des eingeloggten Users
- session['user_email'] : E-Mail des eingeloggten Users
- session['username'] : Username des eingeloggten Users

Nutzer wird per LoginManager von Flask-Login verwaltet.

"""

#Import Flask
from flask import render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_user, current_user
from . import login_blueprint, login_data_require_blueprint
from flask_bcrypt import Bcrypt
from utils.UserMixin import User

from utils.get_datetime import get_current_datetime

#Importiere das Formular
from forms.Login_Form import LoginForm

#Importiere die Datenbankklasse
from data.student_database import DatabaseStudent
from data.admin_database import DatabaseAdmin

bcrypt = Bcrypt()
db = DatabaseStudent("student")
admin_db = DatabaseAdmin("admin")

#Erstellt die Verbindung zur HTML Datei her
@login_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    return render_template('login.html', 
                            form=form,)

# Überprüft die Login-Daten via API
@login_data_require_blueprint.route('/require', methods=['POST'])
def login_require():
    form = LoginForm()
    #Wenn das Formular nicht validiert wird, Fehler zurückgeben
    if not form.validate_on_submit():
        return jsonify({"status": "error", "message": "Ungültige Eingabedaten."}), 400
    
    # Holt die JSON-Daten aus der Anfrage
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400

    # Extrahiert E-Mail und Passwort
    email = data.get('email')
    password = data.get('password')

    find_student = db.find_student_by_email(email)
    find_admin = admin_db.find_admin_by_email(email)
    
    if find_student:
        # Überprüft, ob das Konto verifiziert ist
        if find_student["verification"]["is_verify"] == False:
            return jsonify({"status": "error", "message": "Konto nicht verifiziert."}), 403

        students_password = db.get_students_password(email)

        # Überprüft das Passwort
        if find_student and bcrypt.check_password_hash(students_password, password):
            # Benutzer einloggen
            try:
                user = User(find_student)
                login_user(user)
                print(f"Student eingeloggt. {user.username}")
            except Exception as e:
                print(f"Fehler beim Einloggen des Benutzers: {e}")

            # Session-Daten setzen
            session['logged_in'] = True
            session['user_uuid'] = find_student['uuid']
            session['user_email'] = find_student['email']
            session['username'] = find_student['username']

            # Metadaten updaten
            current_logins = find_student["metadata"]["logins"]
            db.update_student_data(find_student['uuid'], {"metadata.logins": current_logins + 1})
            db.update_student_data(find_student['uuid'], {"metadata.lastLogin": get_current_datetime()})

            return jsonify({"status": "success", "message": "Login erfolgreich."}), 200
        else:
            # Falsches Passwort
            return jsonify({"status": "error", "message": "Falsches Passwort."}), 401
    elif find_admin:
        
        if find_admin["verification"]["is_verify"] == False:
            return jsonify({"status": "error", "message": "Konto nicht verifiziert."}), 403
        
        admins_password = admin_db.get_admins_password(email)

        # Überprüft das Passwort
        if find_admin and bcrypt.check_password_hash(admins_password, password):
            # Benutzer einloggen
            try:  
                user_admin = User(find_admin)
                login_user(user_admin)
                print(f"Admin eingeloggt. {user_admin.username}")
            except Exception as e:
                print(f"Fehler beim Einloggen des Benutzers: {e}")

            # Session-Daten setzen
            session['logged_in'] = True
            session['user_uuid'] = find_admin['uuid']
            session['user_email'] = find_admin['email']
            session['username'] = find_admin['username']

            # Metadaten updaten
            current_logins = find_admin["metadata"]["logins"]
            admin_db.update_admin_data(find_admin['uuid'], {"metadata.logins": current_logins + 1})
            admin_db.update_admin_data(find_admin['uuid'], {"metadata.lastLogin": get_current_datetime()})

            return jsonify({"status": "success", "message": "Login erfolgreich."}), 200
        else:
            # Falsches Passwort
            return jsonify({"status": "error", "message": "Falsches Passwort."}), 401
    else:
        # Benutzer nicht gefunden
        return jsonify({"status": "error", "message": "Benutzer nicht gefunden."}), 404