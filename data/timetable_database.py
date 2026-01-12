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
        week_days,
        #Optionale Felder
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
    ):
        timetable_data = {
            "uuid": uuid, #UUID des Stundenplans
            "classId": class_id, #UUID der Klasse
            "weekDays": week_days, #Liste der Wochentage mit den jeweiligen Stundenplänen
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
    
    # Erstellt ein Formular für eine einzelne Unterrichtsstunde
    def timetable_period_formular(self, 
                                    subject,
                                    teacher,
                                    note,
                                    homework,
                                    start_time,
                                    end_time,):
        
        period_data = {
            "subject": subject, #Fach
            "teacher": teacher, #Lehrer ID
            "note": note, #Notizen
            "homework": homework, #Hausaufgaben
            "startTime": start_time, #Startzeit
            "endTime": end_time, #Endzeit
        }
        return period_data
    
    # Erstellt ein Formular für einen Wochentag im Stundenplan
    def timetable_week_formular(day,periods):
        
        week_day_data = {
            "day": day, #Wochentag
            "periods": periods, #Dict mit den Stunden des Tages
        }
        return week_day_data
    
    