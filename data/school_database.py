"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

from .student_database import DatabaseStudent

class DatabaseSchool(DatabaseStudent):
    def __init__(self, collection_name):
        super().__init__(collection_name)
    
    def school_formular(
        self,
        uuid,
        school_name,
        street,
        house_number,
        city,
        state,
        zip_code,
        country,
        emails,
        school_leader,
        #Optionale Felder
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
        upgradeBy=None,
        phone_numbers=[],
        schoolManagers=[],
        schoolAdmins=[],
        schoolTeachers=[],
        schoolStudents=[],
    ):
        school_data = {
            "uuid": uuid, #UUID der Schule
            "schoolName": school_name,
            "address": {
                "street": street,
                "houseNumber": house_number,
                "city": city,
                "state": state,
                "zipCode": zip_code,
                "country": country,
            },
            "phoneNumbers": phone_numbers, #soll eine Liste sein
            "emails": emails, #soll eine Liste sein
            "schoolMembers": {
                "schoolLeader": school_leader,
                "SchoolManagers": schoolManagers,
                "schoolAdmins": schoolAdmins,
                "schoolTeachers": schoolTeachers,
                "schoolStudents": schoolStudents,
            },
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at,
                "upgradeBy": upgradeBy
            },
            "classes": [] #Hier kommen dann die Klassen ID's rein
            
        }
        return school_data
    
    def create_school(self, school_data):
        # Fügt eine neue Schule zur Datenbank hinzu
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if school_data is None:
            raise ValueError("Schuldaten dürfen nicht None sein.")
        try:
            create_school = self.client[self.database][self.collection].insert_one(school_data)
            if create_school:
                print("Neue Schule erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen der neuen Schule.")
            return
        except Exception as e:
            print(f"Fehler beim Erstellen der neuen Schule: {e}")
            return
    
    def update_school_data(self, uuid, update_data):
        # Aktualisiert die Daten einer Schule in der Datenbank
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
                print("Schuldaten erfolgreich aktualisiert.")
            else:
                print("Keine Änderungen an den Schuldaten vorgenommen.")
            return
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Schuldaten: {e}")
            return
    
    def find_school_by_uuid(self, uuid):
        # Sucht eine Schule in der Datenbank anhand der UUID
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        if uuid is None:
            raise ValueError("UUID darf nicht None sein.")

        school = self.client[self.database][self.collection].find_one({"uuid": uuid})

        if school:
            print("Schule gefunden.")
            return school
        else:
            print("Schule nicht gefunden.")
            return False
    
    def find_school_by_email(self, email):
        # Sucht eine Schule in der Datenbank anhand der E-Mail
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        school = self.client[self.database][self.collection].find_one({"emails": email})

        if school:
            print("Schule gefunden.")
            return school
        else:
            print("Schule nicht gefunden.")
            return False
    
    def find_school_by_name(self, school_name):
        # Sucht eine Schule in der Datenbank anhand des Schulnamens
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        school = self.client[self.database][self.collection].find_one({"schoolName": school_name})

        if school:
            print("Schule gefunden.")
            return school
        else:
            print("Schule nicht gefunden.")
            return False