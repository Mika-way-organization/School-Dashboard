"""Login Page

Wichtige Sache zum Login Bereich.

Es gibt nur diese Sessions:
- session['logged_in'] : Bool ob der User eingeloggt ist
- session['user_uuid'] : UUID des eingeloggten Users
- session['user_email'] : E-Mail des eingeloggten Users
- session['username'] : Username des eingeloggten Users

"""

#Import Flask
from flask import render_template, request, flash, redirect, url_for, session
from flask_login import login_user, current_user
from . import login_blueprint
from flask_bcrypt import Bcrypt
from utils.UserMixin import User

from utils.get_datetime import get_current_datetime

#Importiere das Formular
from forms.Login_Form import LoginForm

#Importiere die Datenbankklasse
from data.database import DatabaseStudent

bcrypt = Bcrypt()
db = DatabaseStudent("student")

#Erstellt die Verbindung zur HTML Datei her
@login_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        find_student = db.find_student_by_email(form.email.data)

        # Überprüft, ob der Student existiert
        if not find_student:
            print("Benutzer nicht gefunden:", form.email.data)
            return redirect(url_for('login.index'))
        
        students_password = db.get_students_password(form.email.data)

        if find_student["verification"]["is_verify"] == False:
            flash('Dein Konto ist noch nicht verifiziert. Bitte überprüfe deine E-Mails.', 'warning')
            return redirect(url_for('codeconfirm.index'))

        # Überprüft das Passwort und loggt den Benutzer ein
        if find_student and bcrypt.check_password_hash(students_password, form.password.data):

            user = User(find_student)

            login_user(user, remember=form.remember_me.data)

            session['logged_in'] = True
            session['user_uuid'] = find_student['uuid']
            session['user_email'] = find_student['email']
            session['username'] = find_student['username']
            
            # Aktualisiert die Anzahl der Logins des Benutzers
            current_logins = find_student["metadata"]["logins"]
            db.update_student_data(
                find_student['uuid'],
                {
                    "metadata.logins": current_logins + 1
                }
            )
            
            # Aktualisiert das letzte Login-Datum und die Uhrzeit
            db.update_student_data(
                find_student['uuid'],
                {
                    "metadata.lastLogin": get_current_datetime()
                }
            )

            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Falsches Passwort. Bitte versuche es erneut.', 'danger')
            return redirect(url_for('login.index'))

    return render_template('login.html', 
                            form=form,)