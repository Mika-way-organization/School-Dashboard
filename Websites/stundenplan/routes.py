#Import Flask
from flask import render_template, redirect, url_for
from . import stundenplan_blueprint
from flask_login import current_user

from data.student_database import DatabaseStudent

db = DatabaseStudent("student")

#Erstellt die Verbindung zur HTML Datei her
@stundenplan_blueprint.route('/<user_id>')
def index(user_id):
    #Überprüft, ob der Benutzer angemeldet ist
    if current_user.is_authenticated:
        username = current_user.username
        
        #Stellt sicher, dass der Benutzer nur auf sein eigenes Profil zugreifen kann
        if current_user.id != user_id:
            return redirect(url_for('stundenplan.index', user_id=current_user.id))
        
        user = db.find_student_by_uuid(user_id)
        
        #Wenn der Benutzer nicht gefunden wird, leite zurück zum Dashboard
        if not user:
            return redirect(url_for('dashboard.index'))
        
    else:
        return redirect(url_for('login.index'))
        
    return render_template('stundenplan.html',
                           username=username)