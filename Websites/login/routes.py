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
from . import login_blueprint
from flask_bcrypt import Bcrypt

#Importiere das Formular
from forms.Login_Form import LoginForm

#Importiere die Datenbankklasse
from data.database import Database

bcrypt = Bcrypt()
db = Database("student")

#Erstellt die Verbindung zur HTML Datei her
@login_blueprint.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        find_student = db.find_student_by_email(form.email.data)

        # Überprüft, ob der Student existiert
        if not find_student:
            flash('E-Mail-Adresse nicht gefunden.', 'danger')
            return redirect(url_for('login.index'))
        
        students_password = db.get_students_password(form.email.data)

        # Überprüft das Passwort
        if find_student and bcrypt.check_password_hash(students_password, form.password.data):

            session['logged_in'] = True
            session['user_uuid'] = find_student['uuid']
            session['user_email'] = find_student['email']
            session['username'] = find_student['username']

            flash('Erfolgreich eingeloggt!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Falsches Passwort. Bitte versuche es erneut.', 'danger')
            return redirect(url_for('login.index'))

    return render_template('login.html', 
                           form=form)