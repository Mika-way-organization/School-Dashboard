#Import Flask
from flask import render_template
from flask_login import current_user
from flask_mail import Message

#Import des Bluprints
from . import dashboard_blueprint

#Import der Datums und Zeit Funktionen
from utils.get_datetime import get_date, get_time
from utils.wetterAPI import WetterAPI

wetter = WetterAPI()

#Erstellt die Verbindung zur HTML Datei her
@dashboard_blueprint.route('/')
def index():
    # Überprüft, ob der Benutzer eingeloggt ist und holt den Benutzernamen
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None # Standardmäßig kein Benutzername
    
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
    

    return render_template('dashboard.html', 
                           username = username, 
                           #Time
                           date=date, time=time,
                           #Weather
                           weather_description=weather_description, 
                            icon=icon,
                           temp=temperatur,
                           feels_like=feels_like,
                           humidity=humidity,
                           city=city)