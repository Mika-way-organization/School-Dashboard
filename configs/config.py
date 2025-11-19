"""Modul: config_loader

Funktion: Dieses Modul ist für das sichere Laden kritischer Konfigurationsvariablen aus einer `.env`-Datei in die Laufzeitumgebung der Anwendung verantwortlich.

Prozess:
1.  Es importiert `load_dotenv` zur Aktivierung der `.env`-Datei.
2.  Es ruft anschließend spezifische Schlüssel wie `SECRET_KEY` und `MONGO_URI` über `os.getenv()` ab.

Zweck: Gewährleistung der Trennung von Code und sensiblen Konfigurationsdaten.
"""


import os
from dotenv import load_dotenv

# Stellt sicher, dass die Umgebungsvariablen aus der .env-Datei geladen werden
load_dotenv() 

secret_key = os.getenv("SECRET_KEY")
#str: Enthält den zentralen kryptografischen Schlüssel der Anwendung, geladen aus der Umgebungsvariable 'SECRET_KEY'.

mongo_uri = os.getenv("MONGO_URI")
#str: Enthält die Verbindungszeichenkette für die MongoDB-Datenbank, geladen aus der Umgebungsvariable 'MONGO_URI'.

#Eine Warnung falls ein Umgebungsschlüssel nicht geladen werden konnte.
if not secret_key or not mongo_uri:
    print("WARNUNG: Mindestens ein kritischer Umgebungsschlüssel (SECRET_KEY oder MONGO_URI) konnte nicht geladen werden!")