#Import Flask
from enum import verify

from flask import render_template, redirect, url_for
from . import profile_blueprint
from flask_login import current_user

from data.student_database import DatabaseStudent
from data.teacher_database import DatabaseTeacher
from data.admin_database import DatabaseAdmin
from data.school_database import DatabaseSchool

student_db = DatabaseStudent("student")
teacher_db = DatabaseTeacher("teacher")
admin_db = DatabaseAdmin("admin")
school_db = DatabaseSchool("school")

#Erstellt die Verbindung zur HTML Datei her
@profile_blueprint.route('/<user_id>')
def index(user_id):
    #Überprüft, ob der Benutzer angemeldet ist
    if current_user.is_authenticated:
        username = current_user.username
        email = current_user.email

        #Stellt sicher, dass der Benutzer nur auf sein eigenes Profil zugreifen kann
        if current_user.id != user_id:
            return redirect(url_for('profile.index', user_id=current_user.id))
        
        student = student_db.find_student_by_uuid(user_id)
        teacher = teacher_db.find_teacher_by_uuid(user_id)
        admin = admin_db.find_admin_by_uuid(user_id)


        if student:
            role=student["role"]
            is_verify=student["verification"]["is_verify"]
            schoolName=student["schoolName"]
            firstName=student["profile"]["firstName"]
            lastName=student["profile"]["lastName"]
            createdAt=student["metadata"]["createdAt"]
        elif teacher:
            role=teacher["role"]
            is_verify=teacher["verification"]["is_verify"]
            schoolName=school_db.find_school_by_uuid(teacher["school_uuid"])["schoolName"]
            firstName=teacher["profile"]["firstName"]
            lastName=teacher["profile"]["lastName"]
            createdAt=teacher["metadata"]["createdAt"]
        elif admin:
            role=admin["role"]
            is_verify=admin["verification"]["is_verify"]
            schoolName=admin["schoolName"]
            firstName=admin["profile"]["firstName"]
            lastName=admin["profile"]["lastName"]
            createdAt=admin["metadata"]["createdAt"]
        else:
            role=None
            is_verify=None
            schoolName=None
            firstName=None
            lastName=None
            createdAt=None
        
        #Wenn der Benutzer nicht gefunden wird, leite zurück zum Dashboard
        if not student and not teacher and not admin:
            return redirect(url_for('dashboard.index'))
        
    else:
        return redirect(url_for('login.index'))
        
    return render_template('profil.html',
                           username=username,
                           email=email,
                           role=role,
                           is_verify=is_verify,
                           schoolName=schoolName,
                           firstName=firstName,
                           lastName=lastName,
                           createdAt=createdAt)