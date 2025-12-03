""""Wetter API

In dieser Datei wird eine Klasse geschrieben sein wo die Wetter Daten anhand der Schul Location und Zeit abgerufen werden können.

"""
#Import der notwendigen Module
import requests
#Importiere den Wetter API Schlüssel aus der config Datei
from configs.config import weather_api_key

#Definierung der WetterAPI Klasse
class WetterAPI:
    def __init__(self):
        self.api_key = weather_api_key
        self.base = "https://api.openweathermap.org/data/2.5/weather?"
    
    #Hier wird die Stadt der Schule geholt (Das mit der Datenbank abfrage wird in Zukunft noch hinzugefügt)
    def get_city(self):
        city = "aschaffenburg" #Hier wird dann die Datenbank abfrage hinzukommen
        return city
    
    #Hier hole wird die Einheit (metrisch) festgelegt
    def get_units(self):
        return "metric"
    
    #Hier wird die Sprache (deutsch) festgelegt
    def get_language(self):
        return "de"
    
    #Hier wird die komplette URL gebaut
    def build_url(self):
        city = self.get_city()
        metric = self.get_units()
        lang = self.get_language()
        return f"{self.base}q={city}&appid={self.api_key}&units={metric}&lang={lang}"
    
    #Hier werden die Wetter Daten abgerufen
    def get_data(self):
        request_url = self.build_url()
        response = requests.get(request_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Es ist ein Fehler beim Abfrufen der Wetterdaten aufgetreten. {response.text}")
            return None