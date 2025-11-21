"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""
#Importiert die notwendigen Bibliotheken von PyMongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

#Importiert die MongoDB-Verbindungszeichenkette aus der Konfigurationsdatei
from configs.config import mongo_uri

class Database:
    def __init__(self, collection_name):
        #Initialisiert die Datenbankverbindung
        self.uri = mongo_uri
        self.client = MongoClient(self.uri)

        #überprüft ob ein collection_name angegeben wurde
        if collection_name:
            self.db = self.client[collection_name]
        else:
            self.db = None
    
    def isconnected(self):
        try:
            #Wenn kein collection_name angegeben wurde wird False zurückgegeben
            if self.db is None:
                print("Collection-Name nicht angegeben.")
                return False
            
            #Pingt die Datenbank an um die Verbindung zu überprüfen
            if self.client.admin.command('ping'):
                print("Datenbankverbindung erfolgreich hergestellt.")
                return True
            
        #Fehlerbehandlung für Verbindungsfehler
        except ConnectionFailure:
            print("Server nicht erreichbar.")
            return False
        except Exception as e:
            print(f"Verbindungsfehler: {e}")
            return False
    
    def get_collection(self):
        #Gibt die aktuelle Datenbank-Collection zurück
        return self.db
    
    def close_connection(self):
        #Schließt die Datenbankverbindung
        self.client.close()