"""Datenbank verknüpfung

In dieser Datei wird die Datenbank verknüpft und verschiedene Funktionen bereitgestellt.

"""

# Importiert Hilfsfunktionen
from utils.get_datetime import get_current_datetime

from student_database import DatabaseStudent

# Erstellt ein Formular für die Admin-Daten
class DatabaseAdmin(DatabaseStudent):
    def __init__(self, collection_name):
        super().__init__(collection_name)
        
    def admin_formular(
        uuid,
        username,
        email,
        password,
        secure_password,
        first_name,
        last_name,
        
        #Optionale Felder
        expiresBy=None,
        is_verify=False,
        avatar=None,
        date_of_birth=None,
        phone_number=None,
        permissions=[],
        created_at=get_current_datetime(),
        updated_at=get_current_datetime(),
        last_login=None,
        logins=0,
        expiresAt=None,
        verifiedAt=None,
        code=None,
        
    ):
        
        admin_formular = {
            "uuid": uuid,
            "username": username,
            "email": email,
            "password": password,
            "secure_password": secure_password,
            "role": "admin",
            "status": "inactive",
            "is_verify": is_verify,
            "profile": {
                "firstName": first_name,
                "lastName": last_name,
                "avatar": avatar,
                "dateOfBirth": date_of_birth,
                "phoneNumber": phone_number,
            },
            "metadata": {
                "createdAt": created_at,
                "updatedAt": updated_at,
                "lastLogin": last_login,
                "logins": logins
            },
            "permissions_admin": permissions,
            "verification": {
                "code": code,
                "expiresBy": expiresBy,
                "expiresAt": expiresAt,
                "verifiedAt": verifiedAt,
                "is_verify": is_verify
            }
        }
        return admin_formular
    
    def create_admin(self, admin_data):
        # Fügt einen neuen Admin zur Datenbank hinzu
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if admin_data is None:
            raise ValueError("Admin-Daten dürfen nicht None sein.")
        try:
            create_admin = self.client[self.database][self.collection].insert_one(admin_data)
            if create_admin:
                print("Neuer Admin erfolgreich erstellt.")
            else:
                print("Fehler beim Erstellen des neuen Admins.")
            return
        except Exception as e:
            print(f"Fehler beim Erstellen des neuen Admins: {e}")
            return
        
    def get_admins_password(self, email):
        # Ruft das Passwort eines Admins anhand der E-Mail-Adresse ab
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")
        if email is None:
            raise ValueError("E-Mail-Adresse darf nicht None sein.")

        admin = self.client[self.database][self.collection].find_one({"email": email}, {"password": 1})

        if admin:
            return admin['password']
        else:
            print("Admin nicht gefunden.")
            return None
    
    def update_admin_data(self, uuid, update_data):
        # Aktualisiert die Daten eines Admins in der Datenbank
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
                print("Admin-Daten erfolgreich aktualisiert.")
            else:
                print("Keine Änderungen an den Admin-Daten vorgenommen.")
            return
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Admin-Daten: {e}")
            return
    
    def find_admin_by_uuid(self, uuid):
        # Sucht einen Admin in der Datenbank anhand der UUID
        if self.collection is None:
            raise ValueError("Datenbankverbindung nicht hergestellt.")

        if uuid is None:
            raise ValueError("UUID darf nicht None sein.")

        admin = self.client[self.database][self.collection].find_one({"uuid": uuid})

        if admin:
            print("Admin gefunden.")
            return admin
        else:
            print("Admin nicht gefunden.")
            return False