#Import Flask
from flask import render_template, redirect, url_for
from . import teacher_blueprint
from flask_login import current_user

from data.student_database import DatabaseStudent
from data.admin_database import DatabaseAdmin
from data.teacher_database import DatabaseTeacher

db = DatabaseStudent("student")
admin_db = DatabaseAdmin("admin")
teacher_db = DatabaseTeacher("teacher")

#Erstellt die Verbindung zur HTML Datei her
@teacher_blueprint.route('/<user_id>')
def index(user_id):
    #Überprüft, ob der Benutzer angemeldet ist
    if current_user.is_authenticated:
        username = current_user.username
        role = current_user.role
        
        #Stellt sicher, dass der Benutzer nur auf sein eigenes Profil zugreifen kann
        if current_user.id != user_id:
            return redirect(url_for('teacherpanel.index', user_id=current_user.id))
        
        teacher = teacher_db.find_teacher_by_uuid(user_id)
        
        #Wenn der Benutzer nicht gefunden wird, leite zurück zum Dashboard
        if not teacher:
            return redirect(url_for('dashboard.index'))
        
    else:
        return redirect(url_for('login.index'))
        
    return render_template('teacherpanel.html',
                           username=username, 
                           role=role)