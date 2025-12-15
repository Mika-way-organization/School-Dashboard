"""Jokes API

In dieser Datei werden Jokes von einer API geholt und random ausgegeben
"""
#Import der notwendigen Module
import requests
import random

#Definierung der Jokes Klasse
class Jokes:
    def __init__(self):
        self.url = "https://v2.jokeapi.dev/joke/Any?lang=de&type=single"
    
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