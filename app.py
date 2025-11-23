"""Welcome

Dies hier ist unser School-Dashboard Projekt.
Die app.py dient als Einstiegspunkt unserer Anwendung, von wo aus die Website gestartet und alle Blueprints initialisiert werden.

"""

#Import Flask (Die Hauptfunktion) und andere notwendige Module
from flask import Flask, redirect, url_for, session
from flask_wtf import CSRFProtect
from flask_bcrypt import Bcrypt
from datetime import timedelta

#Import der Bluprints
from Websites.dashboard import dashboard_blueprint
from Websites.page_not_found import page_not_found_blueprint
from Websites.register_student import register_student_blueprint
from Websites.login import login_blueprint

#import der Konfigurationsvariablen
from configs.config import isConfig_loaded, secret_key, debug_mode

#Import der Datenbankklasse und gibt db eine Verbindung zur Datenbank
from data.database import Database

#Initialisierung der Datenbankverbindung
db = Database("student")

#Hauptfunktion
def create_app(debug = debug_mode):
    #Erstellen der Flask App und Konfigurationen
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = secret_key
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

    #Initialisierung von Bcrypt für die Passwort-Hashing
    bcrypt = Bcrypt(app)
    #Schutz vor CSRF-Angriffen
    csrf = CSRFProtect(app)

    #Registrierung der Blueprints
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
    app.register_blueprint(page_not_found_blueprint, url_prefix="/page_not_found")
    app.register_blueprint(register_student_blueprint, url_prefix="/register_student")
    app.register_blueprint(login_blueprint, url_prefix="/login")

    #Wenn keine Website gefunden wurde, ruft der Server diese Website auf.
    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for("page_not_found.index"))
    
    #Abmelden Route - Löscht die Session und leitet auf die Mainpage weiter
    @app.route("/logout/")
    def logout():
        session.clear()
        return redirect(url_for("dashboard.index"))
    
    #Läd unser Dashboard (Mainpage)
    @app.route("/")
    def root_redirect():
        return redirect(url_for("dashboard.index"))
    
    return app

#Ausführen des Servers
if __name__ == "__main__":
    #Überprüft ob die kritischen Umgebungsvariablen geladen wurden
    isConfig_loaded()

    #Überprüft die Datenbankverbindung
    db.isconnected()

    #Erstellen und Ausführen der App
    app = create_app()
    app.run()