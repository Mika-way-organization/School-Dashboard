"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

from .student_database import DatabaseStudent

# Erstellt ein Formular für die Lehrerdaten
class DatabaseTeacher(DatabaseStudent):
    def __init__(self, collection_name):
        super().__init__(collection_name)
        
    def teacher_formular(
        uuid,
        username,
        email,
        password,
        first_name,
        last_name,
        school_name,
        
        #Optionale Felder
        is_verify=False,
        avatar=None,
        title=None,
        date_of_birth=None,
        phone_number=None,
        subject=[],
        assignedClasses=[],
        mentoredClass=None,
        permissions=[],
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
        last_login=None,
        logins=0,
        expiresAt=None,
        verifiedAt=None,
        code=None,
        
    ):
        
        teacher_data = {
            "uuid": uuid,
            "username": username,
            "email": email,
            "password": password,
            "role": "teacher",
            "status": "inactive",
            "is_verify": is_verify,
            "schoolName": school_name,
            "profile": {
                "firstName": first_name,
                "lastName": last_name,
                "avatar": avatar,
                "title": title,
                "dateOfBirth": date_of_birth,
                "phoneNumber": phone_number,
            },
            "teaching_data": {
                "subjects": subject,
                "assignedClasses": assignedClasses,
                "mentoredClass": mentoredClass,
            },
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at,
                "lastLogin": last_login,
                "logins": logins
            },
            "permissions": permissions,
            "verification": {
                "code": code,
                "expiresAt": expiresAt,
                "verifiedAt": verifiedAt,
                "is_verify": is_verify
            }
        }
        return teacher_data
    
    def create_teacher(self, teacher_data):
        # Fügt einen neuen Lehrer zur Datenbank hinzu
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if teacher_data is None:
            raise ValueError("Lehrerdaten dürfen nicht None sein.")
        try:
            create_teacher = self.client[self.database][self.collection].insert_one(teacher_data)
            if create_teacher:
                print("Neuer Lehrer erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen des neuen Lehrers.")
            return
        except Exception as e:
            print(f"Fehler beim Erstellen des neuen Lehrers: {e}")
            return
    
    def get_teachers_password(self, email):
        # Ruft das Passwort eines Lehrers anhand der E-Mail-Adresse ab
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if email is None:
            raise ValueError("E-Mail-Adresse darf nicht None sein.")

        teacher = self.client[self.database][self.collection].find_one({"email": email}, {"password": 1})

        if teacher:
            return teacher['password']
        else:
            print("Lehrer nicht gefunden.")
            return None
    
    def update_teacher_data(self, uuid, update_data):
        # Aktualisiert die Daten eines Lehrers in der Datenbank
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
                print("Lehrerdaten erfolgreich aktualisiert.")
            else:
                print("Keine Änderungen an den Lehrerdaten vorgenommen.")
            return
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Lehrerdaten: {e}")
            return
    
    def find_teacher_by_uuid(self, uuid):
        # Sucht einen Lehrer in der Datenbank anhand der UUID
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        if uuid is None:
            raise ValueError("UUID darf nicht None sein.")

        teacher = self.client[self.database][self.collection].find_one({"uuid": uuid})

        if teacher:
            print("Lehrer gefunden.")
            return teacher
        else:
            print("Lehrer nicht gefunden.")
            return False
