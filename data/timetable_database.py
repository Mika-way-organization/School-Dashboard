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
    
    # Erstellt ein Formular für den Stundenplan
    def timetable_formular(
        self,
        uuid,
        class_id,
        date,
        subject,
        teacher,
        note,
        homework,
        lesson_hour,
        #Optionale Felder
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
    ):
        timetable_data = {
            "uuid": uuid, #UUID des Stundenplans
            "classId": class_id, #UUID der Klasse
            "date": date, #Datum des Stundenplans
            "schedule": {
                "subject": subject, #Fach
                "teacher": teacher, #Lehrer ID
                "note": note, #Notizen
                "homework": homework, #Hausaufgaben
                "lesson_hour": lesson_hour, #Untterrichtsstunde
            },
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
            create_timetable = self.client[self.database][self.collection].insert_one(timetable_data)
            if create_timetable:
                print("Stundenplan erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen des Stundenplans.")
        except Exception as e:
            raise Exception(f"Fehler beim Erstellen des Stundenplans: {e}")
    
    def find_timetable_by_date(self, class_id, date):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        
        try:
            timetable = self.client[self.database][self.collection].find_one({
                "classId": class_id,
                "date": date
            })
            if timetable:
                print("Stundenplan gefunden.")
                return timetable
            else:
                print("Kein Stundenplan für das angegebene Datum gefunden.")
                return None
        except Exception as e:
            raise Exception(f"Fehler beim Abrufen des Stundenplans: {e}")
    
    def update_timetable(self, class_id, date, updated_data):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        
        if updated_data is None:
            raise ValueError("Ungültige aktualisierte Daten.")
        
        try:
            update_result = self.client[self.database][self.collection].update_one(
                {
                    "classId": class_id,
                    "date": date
                },
                {
                    "$set": updated_data
                }
            )
            if update_result.modified_count > 0:
                print("Stundenplan erfolgreich aktualisiert.")
            else:
                print("Kein Stundenplan aktualisiert. Möglicherweise wurden keine Änderungen vorgenommen.")
        except Exception as e:
            raise Exception(f"Fehler beim Aktualisieren des Stundenplans: {e}")
    
    