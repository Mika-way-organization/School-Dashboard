#Import Flask
from flask import render_template
from flask_login import current_user
from flask_mail import Message
import random

from data.student_database import DatabaseStudent
from data.admin_database import DatabaseAdmin
from data.teacher_database import DatabaseTeacher
from data.timetable_database import DatabaseTimetable
from data.school_database import DatabaseSchool
from data.class_database import DatabaseClasses

student_db = DatabaseStudent("student")
class_db = DatabaseClasses("class")
teacher_db = DatabaseTeacher("teacher")
timetable_db = DatabaseTimetable("timetable")

#Import des Bluprints
from . import dashboard_blueprint

#Import der Datums und Zeit Funktionen
from utils.get_datetime import get_date, get_time, get_datetime_formatted, get_current_time_format
from utils.wetterAPI import WetterAPI
from utils.jokesAPI import Jokes

wetter = WetterAPI()
jokes = Jokes()

#Erstellt die Verbindung zur HTML Datei her
@dashboard_blueprint.route('/')
def index():
    # Überprüft, ob der Benutzer eingeloggt ist und holt den Benutzernamen
    if current_user.is_authenticated:
        username = current_user.username
        role = current_user.role

        user_id = current_user.id

        global class_data
        global timetable_data
        
        today = get_datetime_formatted()
        now_time = get_current_time_format()
        current_lesson_hour = get_lesson_hour(now_time)
        
        if current_lesson_hour is not None:
            if role == "student":
                student_data = student_db.find_student_by_uuid(user_id)
                if student_data:
                    student_class = student_data['classData']['classID']
                    class_data = class_db.find_class_by_uuid(student_class)
                    if class_data:
                        print("Klasse des Schülers gefunden:", class_data['className'])
                        
                        for timetable_id in class_data['timetableID']:
                            timetable_data = timetable_db.find_timetable_by_uuid(timetable_id)
                            if timetable_data:
                                print("Stundenplandaten gefunden für ID:", timetable_id)
                                
                                timetable_today = timetable_db.find_timetable_by_uuid_and_date(timetable_id, today)
                                if timetable_today:
                                    timetable_now = timetable_db.find_timetable_by_uuid_and_date_and_hour(timetable_id, today, current_lesson_hour)
                                    
                                    if timetable_now:
                                        timetable_data = timetable_now
                                        print("Aktuelle Stunde gefunden für ID:", timetable_id)
                                    else:
                                        print("Keine aktuelle Stunde, aber heutiger Stundenplan gefunden für ID:", timetable_id)
                                    
                                    print("Heutiger Stundenplan gefunden für ID:", timetable_id)
                            else:
                                print("Kein Stundenplan gefunden für ID:", timetable_id)
                        else:
                            print("Keine Stundenplan für den Schüler gefunden.")


            elif role == "teacher":
                teacher_data = teacher_db.find_teacher_by_uuid(user_id)
                if teacher_data:
                    class_data = class_db.find_class_by_teacher_id(user_id)
                    if class_data:
                        print("Klasse des Lehrers gefunden:", class_data['className'])
                        
                        for timetable_id in class_data['timetableID']:
                            timetable_data = timetable_db.find_timetable_by_uuid(timetable_id)
                            if timetable_data:
                                print("Stundenplandaten gefunden für ID:", timetable_id)
                                
                                timetable_today = timetable_db.find_timetable_by_uuid_and_date(timetable_id, today)
                                if timetable_today:
                                    
                                    timetable_now = timetable_db.find_timetable_by_uuid_and_date_and_hour(timetable_id, today, current_lesson_hour)
                                    
                                    if timetable_now:
                                        timetable_data = timetable_now
                                        print("Aktuelle Stunde gefunden für ID:", timetable_id)
                                    else:
                                        print("Keine aktuelle Stunde für ID:", timetable_id)
                                        
                                    print("Heutiger Stundenplan gefunden für ID:", timetable_id)
                            else:
                                print("Kein Stundenplan gefunden für ID:", timetable_id)
                        else:
                            print("Keine Stundenplan für den Lehrer gefunden.")


            elif role == "admin":
                pass
            
        else:
            timetable_data = None
            print("Derzeit keine laufende Unterrichtsstunde.")
        


    else:
        username = None # Standardmäßig kein Benutzername
        role = None
    
    # Holt das aktuelle Datum und die aktuelle Uhrzeit
    date = get_date()
    time = get_time()
    
    # Holt die Wetterdaten
    data = wetter.get_data()
    w_data = data['weather']
    w_list = w_data[0]
    weather_description = w_list['description']
    icon = w_list['icon']
    temperatur = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    city = data['name']
    
    #Witze API
    joke = jokes.get_joke()
    joke2 = jokes.get_antoher_Joke()
    joke_list = [joke, joke2]
    selected_joke = random.choice(joke_list)
    if selected_joke == False:
        selected_joke = jokes.get_joke()
        print("Fehler beim Abrufen des Witzes von www.schul-dashboard.de")

    #Klassen Daten für Stundenplan abrufen
    if timetable_data is not None:
        subject = timetable_data["subject"]
        teacher_id = timetable_data["teacher"]
        room = timetable_data["room"]
        note = timetable_data["note"]
        homework = timetable_data["homework"]
    else:
        subject = None
        teacher_id = None
        room = None
        note = None
        homework = None
    

    return render_template('dashboard.html', 
                           username = username,
                           role = role,
                           #Time
                           date=date, time=time,
                           #Weather
                           weather_description=weather_description, 
                            icon=icon,
                           temp=temperatur,
                           feels_like=feels_like,
                           humidity=humidity,
                           city=city,
                           #Joke
                           joke=selected_joke,
                           #Stundenplan
                           subject=subject,   
                           teacher_id=teacher_id,
                           room=room,
                           note=note,
                           homework=homework)

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