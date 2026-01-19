"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

from .student_database import DatabaseStudent


# Erstellt ein Formular für die Stundenplan-Daten
class DatabaseTimetable(DatabaseStudent):
    def __init__(self, collection_name):
        super().__init__(collection_name)

    # Erstellt ein Formular für den Stundenplan (Neu)
    def timetable_formular(
        self,
        uuid,
        class_id,
        date,
        # Optionale Felder
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
    ):
        timetable_data = {
            "uuid": uuid,  # UUID des Stundenplans
            "classId": class_id,  # UUID der Klasse
            "date": date,  # Datum des Stundenplans
            "schedule": [],
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at,
            },
        }
        return timetable_data
    
    def create_timetable(self, timetable_data):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")

        if timetable_data is None:
            raise ValueError("Ungültige Stundenplandaten.")
        try:
            create_timetable = self.client[self.database][self.collection].insert_one(
                timetable_data
            )
            if create_timetable:
                print("Stundenplan erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen des Stundenplans.")
        except Exception as e:
            raise Exception(f"Fehler beim Erstellen des Stundenplans: {e}")

    def add_schedule_entry(
        self,
        class_id,
        date,
        subject,
        teacher,
        room,
        note,
        homework,
        lesson_hour,
    ):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        
        schedule_entry = {
            "subject": subject,  # Fach
            "teacher": teacher,  # Lehrer ID
            "room": room, # Raum
            "note": note,  # Notizen
            "homework": homework,  # Hausaufgaben
            "lesson_hour": lesson_hour,  # Untterrichtsstunde
        }

        try:
            update_result = self.client[self.database][self.collection].update_one(
                {"classId": class_id, "date": date},
                {"$push": {"schedule": schedule_entry}},
            )
            if update_result.modified_count > 0:
                print("Stundenplan-Eintrag erfolgreich hinzugefügt.")
            else:
                print("Kein Stundenplan-Eintrag hinzugefügt. Möglicherweise wurden keine Änderungen vorgenommen.")
        except Exception as e:
            raise Exception(f"Fehler beim Hinzufügen des Stundenplan-Eintrags: {e}")
    
    def update_schedule_entry(
        self,
        class_id,
        date,
        subject,
        teacher,
        room,
        note,
        homework,
        lesson_hour,
    ):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        
        try:
            update_result = self.client[self.database][self.collection].update_one(
                {"classId": class_id, "date": date, "schedule.lesson_hour": lesson_hour},
                {"$set": {
                    "schedule.$.subject": subject,
                    "schedule.$.teacher": teacher,
                    "schedule.$.room": room,
                    "schedule.$.note": note,
                    "schedule.$.homework": homework,
                }},
            )
            if update_result.modified_count > 0:
                print("Stundenplan-Eintrag erfolgreich aktualisiert.")
            else:
                print("Kein Stundenplan-Eintrag aktualisiert. Möglicherweise wurden keine Änderungen vorgenommen.")
        except Exception as e:
            raise Exception(f"Fehler beim Aktualisieren des Stundenplan-Eintrags: {e}")
        
    def find_timetable_by_class_and_date_and_hour(self, class_id, date, lesson_hour):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")

        try:
            timetable = self.client[self.database][self.collection].find_one(
                {"classId": class_id, "date": date, "schedule.lesson_hour": lesson_hour}
            )
            
            if timetable:
                for entry in timetable.get("schedule", []):
                    if entry.get("lesson_hour") == lesson_hour:
                        print("Stundenplan-Eintrag erfolgreich abgerufen.")
                        return entry
            else:
                print("Kein Stundenplan-Eintrag gefunden.")
                return None
            
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Stundenplans: {e}")
    
    def find_timetable_by_class_and_date(self, class_id, date):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")

        try:
            timetable = self.client[self.database][self.collection].find_one(
                {"classId": class_id, "date": date}
            )
            
            if timetable:
                print("Stundenplan erfolgreich abgerufen.")
                return timetable
            else:
                print("Kein Stundenplan gefunden.")
                return None
            
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Stundenplans: {e}")
    
    def find_timetable_by_uuid(self, uuid):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")

        try:
            timetable = self.client[self.database][self.collection].find_one(
                {"uuid": uuid}
            )
            
            if timetable:
                print("Stundenplan erfolgreich abgerufen.")
                return timetable
            else:
                print("Kein Stundenplan gefunden.")
                return None
            
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Stundenplans: {e}")
    
    def find_timetable_by_uuid_and_date(self, uuid, date):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")

        try:
            timetable = self.client[self.database][self.collection].find_one(
                {"uuid": uuid, "date": date}
            )
            
            if timetable:
                print("Stundenplan erfolgreich abgerufen.")
                return timetable
            else:
                print("Kein Stundenplan gefunden.")
                return None
            
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Stundenplans: {e}")
    
    def find_timetable_by_uuid_and_date_and_hour(self, uuid, date, lesson_hour):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")

        try:
            timetable = self.client[self.database][self.collection].find_one(
                {"uuid": uuid, "date": date, "schedule.lesson_hour": lesson_hour}
            )
            
            if timetable:
                for entry in timetable.get("schedule", []):
                    if entry.get("lesson_hour") == lesson_hour:
                        print("Stundenplan-Eintrag erfolgreich abgerufen.")
                        return entry
            else:
                print("Kein Stundenplan-Eintrag gefunden.")
                return None
            
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Stundenplans: {e}")