"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

from student_database import DatabaseStudent

class DatabaseClasses(DatabaseStudent):
    def __init__(self, collection_name):
        super().__init__(collection_name)
    
    def class_formular(
        uuid,
        class_name,
        grade_level,
        section,
        school_id,
        class_teacher_id,
        timetableID,
        #Optionale Felder
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
            "classTeacherId": class_teacher_id,
            "students": students, #Liste der Schüler UUID's
            "subjects": subjects, #Liste der Fächer
            "timetableID": timetableID, #Hier wird die ID des Stundenplans gespeichert
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at,
            },
        }
        return class_data