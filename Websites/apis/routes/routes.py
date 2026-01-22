from flask_login import current_user

#Import des Blueprints
from . import dashboard_data_blueprint
import random

#Import der Datums und Zeit Funktionen
from utils.get_datetime import get_date, get_time, get_datetime_formatted, get_current_time_format
from utils.wetterAPI import WetterAPI
from utils.jokesAPI import Jokes

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

wetter = WetterAPI()
jokes = Jokes()

#Die API gibt die Daten für das Dashboard zurück
@dashboard_data_blueprint.route("/")
def dashboard_data():
    # Überprüft, ob der Benutzer eingeloggt ist und holt den Benutzernamen
    if current_user.is_authenticated:
        role = current_user.role

        user_id = current_user.id

        global class_data
        global timetable_data
        is_lesson_now = False
        
        today = get_datetime_formatted()
        now_time = get_current_time_format()
        current_lesson_hour = get_lesson_hour(now_time)
        print("Aktuelle Uhrzeit:", now_time)
        print("Aktuelle Unterrichtsstunde:", current_lesson_hour)

        timetable_data = get_current_lesson(user_id, role, current_lesson_hour, today)
        if timetable_data is not None:
            is_lesson_now = True
        


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

    #Klassen Daten für Stundenplan abrufen
    if timetable_data is not None and is_lesson_now:
        subject = timetable_data["subject"]
        teacher_id = timetable_data["teacher"]
        room = timetable_data["room"]
        note = timetable_data["note"]
        homework = timetable_data["homework"]
        first_lesson = get_current_lesson(user_id, role, 1, today)
        second_lesson = get_current_lesson(user_id, role, 2, today)
        third_lesson = get_current_lesson(user_id, role, 3, today)
        fourth_lesson = get_current_lesson(user_id, role, 4, today)
        fifth_lesson = get_current_lesson(user_id, role, 5, today)
        sixth_lesson = get_current_lesson(user_id, role, 6, today)
        seventh_lesson = get_current_lesson(user_id, role, 7, today)
        eighth_lesson = get_current_lesson(user_id, role, 8, today)
        ninth_lesson = get_current_lesson(user_id, role, 9, today)
        tenth_lesson = get_current_lesson(user_id, role, 10, today)
    else:
        subject = None
        teacher_id = None
        room = None
        note = None
        homework = None
        first_lesson = None
        second_lesson = None
        third_lesson = None
        fourth_lesson = None
        fifth_lesson = None
        sixth_lesson = None
        seventh_lesson = None
        eighth_lesson = None
        ninth_lesson = None
        tenth_lesson = None
    
    data_dict = {
        "date": date,
        "time": time,
        "weather_description": weather_description,
        "icon": icon,
        "temperatur": temperatur,
        "feels_like": feels_like,
        "humidity": humidity,
        "city": city,
        "joke": selected_joke,
        "subject": subject,
        "teacher_id": teacher_id,
        "room": room,
        "note": note,
        "homework": homework,
        "first_lesson": first_lesson,
        "second_lesson": second_lesson,
        "third_lesson": third_lesson,
        "fourth_lesson": fourth_lesson,
        "fifth_lesson": fifth_lesson,
        "sixth_lesson": sixth_lesson,
        "seventh_lesson": seventh_lesson,
        "eighth_lesson": eighth_lesson,
        "ninth_lesson": ninth_lesson,
        "tenth_lesson": tenth_lesson
        }
    return data_dict


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