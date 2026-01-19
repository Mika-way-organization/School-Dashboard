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

#Import des Bluprints
from . import dashboard_blueprint

#Import der Datums und Zeit Funktionen
from utils.get_datetime import get_date, get_time
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

        if role == "student":
            db = DatabaseStudent("student")
            student_data = db.find_student_by_uuid(user_id)
            if student_data:
                student_class = student_data['classData']['classID']

                class_db = DatabaseClasses("classes")
                class_data = class_db.find_class_by_uuid(student_class)
                if class_data:
                    print("Klasse des Schülers gefunden:", class_data['className'])

        elif role == "teacher":
            db = DatabaseTeacher("teacher")
            teacher_data = db.find_teacher_by_uuid(user_id)
            if teacher_data:
                teacher_class = teacher_data['classData']['classID']

                class_db = DatabaseClasses("classes")
                class_data = class_db.find_class_by_uuid(teacher_class)
                if class_data:
                    print("Klasse des Lehrers gefunden:", class_data['className'])


        elif role == "admin":
            pass


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
                           joke=selected_joke)