"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert die notwendigen Bibliotheken von PyMongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Importiert die Mongocollection-Verbindungszeichenkette aus der Konfigurationsdatei
from configs.config import mongo_uri

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

# Erstellt die Datenbankklasse für Schüler
class DatabaseStudent:
    def __init__(self, collection_name):
        # Initialisiert die Datenbankverbindung
        self.uri = mongo_uri
        self.client = MongoClient(self.uri)
        self.database = "Schul_Dashboard"

        # überprüft ob ein collection_name angegeben wurde
        if collection_name:
            self.collection = collection_name
        else:
            self.collection = None

    def isconnected(self):
        try:
            # Wenn kein collection_name angegeben wurde wird False zurückgegeben
            if self.collection is None:
                print("Collection-Name nicht angegeben.")
                return False

            # Pingt die Datenbank an um die Verbindung zu überprüfen
            if self.client.admin.command("ping"):
                print("Datenbankverbindung erfolgreich hergestellt.")
                return True

        # Fehlerbehandlung für Verbindungsfehler
        except ConnectionFailure:
            print("Der MongoDB Server ist nicht erreichbar.")
            return False
        except Exception as e:
            print(f"Verbindungsfehler: {e}")
            return False

    def find_student_by_email(self, email):
        # Sucht einen Studenten in der Datenbank anhand der E-Mail-Adresse
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        if email is None:
            raise ValueError("E-Mail-Adresse darf nicht None sein.")

        student = self.client[self.database][self.collection].find_one({"email": email})

        if student:
            print("Student gefunden.")
            return student
        else:
            print("Student nicht gefunden.")
            return False

    def find_student_by_uuid(self, uuid):
        # Sucht einen Studenten in der Datenbank anhand der UUID
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        student = self.client[self.database][self.collection].find_one({"uuid": uuid})

        if student:
            print("Student gefunden.")
            return student
        else:
            print("Student nicht gefunden.")
            return False

    def close_connection(self):
        # Schließt die Datenbankverbindung
        self.client.close()
        print("Datenbankverbindung geschlossen.")
    
    def find_student_by_name(self, username):
        # Sucht einen Studenten in der Datenbank anhand des Benutzernamens
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        student = self.client[self.database][self.collection].find_one({"username": username})

        if student:
            print("Student gefunden.")
            return student
        else:
            print("Student nicht gefunden.")
            return False

    # Erstellt ein Formular für die Schülerdaten
    def student_formular(
        self,
        uuid,
        username,
        email,
        password,
        first_name,
        last_name,
        # Optionale Felder
        school_id=None,
        class_id=None,
        is_verify=False,
        avatar=None,
        grade_level=None,
        section=None,
        class_teacher_id=None,
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
        last_login=None,
        logins=0,
        expiresAt=None,
        verifiedAt=None,
        code=None,
    ):
        student_data = {
            "uuid": uuid,
            "username": username,
            "email": email,
            "password": password,
            "role": "student",
            "status": "inactive",
            "schoolID": school_id,
            "profile": {
                "firstName": first_name,
                "lastName": last_name,
                "avatar": avatar,
            },
            "classData": {
                "classID": class_id,
                "gradeLevel": grade_level,
                "section": section,
                "classTeacherId": class_teacher_id,
            },
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at,
                "lastLogin": last_login,
                "logins": logins
            },
            "verification": {
                "code": code,
                "expiresAt": expiresAt,
                "verifiedAt": verifiedAt,
                "is_verify": is_verify
            }
        }
        return student_data
    
    def create_student(self, student_data):
        # Fügt einen neuen Schüler zur Datenbank hinzu
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if student_data is None:
            raise ValueError("Studentendaten dürfen nicht None sein.")
        try:
            create_student = self.client[self.database][self.collection].insert_one(student_data)
            if create_student:
                print("Neuer Student erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen des neuen Studenten.")
            return
        except Exception as e:
            print(f"Fehler beim Erstellen des neuen Studenten: {e}")
            return
    
    def get_students_password(self, email):
        # Ruft das Passwort eines Schülers anhand der E-Mail-Adresse ab
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if email is None:
            raise ValueError("E-Mail-Adresse darf nicht None sein.")

        student = self.client[self.database][self.collection].find_one({"email": email}, {"password": 1})

        if student:
            return student['password']
        else:
            print("Student nicht gefunden.")
            return None
    
    def update_student_data(self, uuid, update_data):
        # Aktualisiert die Daten eines Schülers in der Datenbank
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if uuid is None:
            raise ValueError("UUID darf nicht None sein.")
        if update_data is None:
            raise ValueError("Aktualisierungsdaten dürfen nicht None sein.")
        
        try:
            update_result = self.client[self.database][self.collection].update_one(
                {"uuid": uuid},
                {"$set": update_data}
            )
            if update_result.modified_count > 0:
                print("Studentendaten erfolgreich aktualisiert.")
            else:
                print("Keine Änderungen an den Studentendaten vorgenommen.")
            return
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Studentendaten: {e}")
            return
    
    def give_all_students_username(self):
        # Gibt alle Schüler in der Datenbank zurück (nur Usernames)
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        
        try:
            # _id: 0 schließt die Object-ID explizit aus
            students = list(self.client[self.database][self.collection].find({}, {"username": 1, "_id": 0}))
            print(f"{len(students)} Schüler gefunden.")
            return students
        except Exception as e:
            print(f"Fehler beim Abrufen der Schüler: {e}")
            return []