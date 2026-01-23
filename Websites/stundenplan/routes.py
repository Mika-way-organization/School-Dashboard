#Import Flask
from flask import render_template, redirect, url_for
from . import stundenplan_blueprint
from flask_login import current_user

from utils import get_datetime

from data.student_database import DatabaseStudent
from data.teacher_database import DatabaseTeacher
from data.school_database import DatabaseSchool
from data.admin_database import DatabaseAdmin
from data.class_database import DatabaseClasses
from data.timetable_database import DatabaseTimetable

student_db = DatabaseStudent("student")
teacher_db = DatabaseTeacher("teacher")
school_db = DatabaseSchool("school")
admin_db = DatabaseAdmin("admin")
class_db = DatabaseClasses("class")
timetable_db = DatabaseTimetable("timetable")

#Erstellt die Verbindung zur HTML Datei her
@stundenplan_blueprint.route('/<user_id>')
def index(user_id):
    #Überprüft, ob der Benutzer angemeldet ist
    if current_user.is_authenticated:
        username = current_user.username
        role = current_user.role
        
        #Stellt sicher, dass der Benutzer nur auf sein eigenes Profil zugreifen kann
        if current_user.id != user_id:
            return redirect(url_for('stundenplan.index', user_id=current_user.id))
        
        student = student_db.find_student_by_uuid(user_id)
        admin = admin_db.find_admin_by_uuid(user_id)
        teacher = teacher_db.find_teacher_by_uuid(user_id)
        
        #Wenn der Benutzer nicht gefunden wird, leite zurück zum Dashboard
        if not student and not admin and not teacher:
            return redirect(url_for('dashboard.index'))
        

        today = get_datetime.get_datetime_formatted()
        now_time = get_datetime.get_current_time_format()
        current_lesson_hour = get_lesson_hour(now_time)
        
    else:
        return redirect(url_for('login.index'))
        
    return render_template('stundenplan.html',
                           username=username,
                           user_id=user_id,
                           role=role,
                           today=today,
                           current_lesson_hour= current_lesson_hour,
                           get_current_day= get_datetime.get_date_of_weekday,
                           get_current_lesson=get_current_lesson)

def get_current_lesson(user_id, role, current_lesson_hour, today):
    # 1. Basis-Validierung
    if current_lesson_hour is None:
        return None

    # 2. Klassen-ID anhand der Rolle ermitteln
    class_data = None
    if role == "student":
        student_data = student_db.find_student_by_uuid(user_id)
        if student_data:
            class_data = class_db.find_class_by_uuid(student_data['classData']['classID'])
    elif role == "teacher":
        class_data = class_db.find_class_by_teacher_id(user_id)

    if not class_data:
        print(f"Keine Klasse für {role} {user_id} gefunden.")
        return None

    print(f"Klasse gefunden: {class_data['className']}")

    # 3. Stundenplan-Logik
    for timetable_id in class_data.get('timetableID', []):
        timetable_now = timetable_db.find_timetable_by_uuid_and_date_and_hour(
            timetable_id, today, current_lesson_hour
        )

        if timetable_now:
            print(f"Aktuelle Stunde gefunden: {timetable_now}")
            return timetable_now

    print("Keine aktuelle Stunde für die IDs gefunden.")
    return None


def get_lesson_hour(current_time):
    
    if current_time >= "08:00" and current_time < "08:45":
        return 1
    elif current_time >= "08:45" and current_time < "09:30":
        return 2
    elif current_time >= "09:30" and current_time < "10:15":
        return 3
    elif current_time >= "10:35" and current_time < "11:20":
        return 4
    elif current_time >= "11:20" and current_time < "12:05":
        return 5
    elif current_time >= "12:40" and current_time < "13:25":
        return 6
    elif current_time >= "13:25" and current_time < "14:10":
        return 7
    elif current_time >= "14:20" and current_time < "15:05":
        return 8
    elif current_time >= "15:05" and current_time < "15:50":
        return 9
    elif current_time >= "16:00" and current_time < "16:45":
        return 10
    else:
        return None