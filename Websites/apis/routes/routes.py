#Import des Blueprints
from . import dashboard_data_blueprint
import random

#Import der Datums und Zeit Funktionen
from utils.get_datetime import get_date, get_time
from utils.wetterAPI import WetterAPI
from utils.jokesAPI import Jokes

wetter = WetterAPI()
jokes = Jokes()

#Die API gibt die Daten für das Dashboard zurück
@dashboard_data_blueprint.route("/")
def dashboard_data():
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
    
    data_dict = {
        "date": date,
        "time": time,
        "weather_description": weather_description,
        "icon": icon,
        "temperatur": temperatur,
        "feels_like": feels_like,
        "humidity": humidity,
        "city": city,
        "joke": selected_joke
        }
    return data_dict