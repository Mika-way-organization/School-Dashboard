"""Jokes API

In dieser Datei werden Jokes von einer API geholt und random ausgegeben
"""
#Import der notwendigen Module
import requests

from configs.config import joke_api_key


#Definierung der Jokes Klasse
class Jokes:
    def __init__(self):
        self.url = "https://v2.jokeapi.dev/joke/Any?lang=de&type=single"
        self.secondUrl = "https://schul-dashboard.ddnss.de/api/joke?api_key="
    
    #Hier werden die Witze abgerufen
    def get_joke(self):
        response = requests.get(self.url)
        try:
            if response.status_code == 200:
                joke_data = response.json()
                
                if joke_data.get("error"):
                    print(f"Fehler von der API: {joke_data.get('message', 'Unbekannter Fehler.')}")
                    return
                
                joke_text = joke_data.get("joke")
                if joke_text:
                    return joke_text
                else:
                    return "Fehler: API lieferte keinen einzelnen Witz-Text."
            else:
                return f"Fehler beim Abrufen des Witzes. Status Code: {response.status_code}"
        
        # Fehlerbehandlung bei Netzwerkproblemen
        except requests.exceptions.RequestException as e:
            return f"Ein Netzwerkfehler ist aufgetreten: {e}"
    
    def get_antoher_Joke(self):
        api_key = joke_api_key
        try:
            response = requests.get(f"{self.secondUrl}{api_key}", timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                
                joke_data = response.json()
                
            if joke_data["data"].get("error"):
                message = joke_data.get("message", "Unbekannter API-Fehler")
                return f"Fehler von der API: {message}"
            
            joke_text = joke_data["data"].get("joke")
            if joke_text:
                return joke_text
            else:
                return False

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP-Fehler aufgetreten: {http_err}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Netzwerkfehler aufgetreten: {e}")
            return False
        except KeyError:
            print("Fehler: Unerwartetes Datenformat der API.")
            return False