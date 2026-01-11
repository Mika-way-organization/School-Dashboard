"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

from .student_database import DatabaseStudent

class DatabaseClasses(DatabaseStudent):
    def __init__(self, collection_name):
        super().__init__(collection_name)
    
    def class_formular(
        self,
        uuid,
        class_name,
        grade_level,
        section,
        school_id,
        class_teacher_id,
        #Optionale Felder
        timetableID="No Timetable Assigned",
        classRoom="No Room Assigned",
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
        students=[],
        subjects=[],
    ):
        class_data = {
            "uuid": uuid, #UUID der Klasse
            "className": class_name,
            "gradeLevel": grade_level,
            "section": section,
            "schoolId": school_id,
            "classRoom": classRoom,
            "classTeacherId": class_teacher_id,
            "students": students, #Liste der Schüler UUID's
            "subjects": subjects, #Liste der Fächer
            "timetableID": timetableID, #Hier wird die ID des Stundenplans gespeichert
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at
            },
        }
        return class_data
    
    def create_class(self, class_data):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        if class_data is None:
            raise ValueError("class_data darf nicht None sein.")
        try:
            create_class = self.client[self.database][self.collection].insert_one(class_data)

            if create_class:
                print("Klasse erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen der Klasse.")

        except Exception as e:
            print(f"Fehler beim Erstellen der Klasse: {e}")
            return
    
    def find_class_by_uuid(self, class_uuid):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        
        class_data = self.client[self.database][self.collection].find_one({"uuid": class_uuid})

        if class_data:
            print("Klasse gefunden.")
            return class_data
        else:
            print("Klasse nicht gefunden.")
            return False
    
    def update_class_data(self, class_uuid, update_data):
        if self.collection is None:
            raise Exception("Datenbankverbindung nicht hergestellt.")
        if class_uuid is None:
            raise ValueError("class_uuid darf nicht None sein.")
        if update_data is None:
            raise ValueError("update_data darf nicht None sein.")
        
        try:
            update_result = self.client[self.database][self.collection].update_one(
                {"uuid": class_uuid},
                {"$set": update_data}
            )

            if update_result.modified_count > 0:
                print("Klassendaten erfolgreich aktualisiert.")
            else:
                print("Keine Änderungen an den Klassendaten vorgenommen.")

        except Exception as e:
            print(f"Fehler beim Aktualisieren der Klassendaten: {e}")
            return
             

