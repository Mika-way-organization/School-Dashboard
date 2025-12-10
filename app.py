"""Welcome

Dies hier ist unser School-Dashboard Projekt.
Die app.py dient als Einstiegspunkt unserer Anwendung, von wo aus die Website gestartet und alle Blueprints initialisiert werden.

"""

#Import Flask (Die Hauptfunktion) und andere notwendige Module
from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, login_required, logout_user
from datetime import timedelta

# Import der Erweiterungen
from extensions import *

#Import der Bluprints
from Websites.dashboard import dashboard_blueprint
from Websites.page_not_found import page_not_found_blueprint
from Websites.register_student import register_student_blueprint, register_data_require_blueprint
from Websites.login import login_blueprint, login_data_require_blueprint
from Websites.profile import profile_blueprint
from Websites.codeconfirm import codeconfirm_blueprint, codeconfirm_data_require_blueprint
from Websites.stundenplan import stundenplan_blueprint

#Import der API Blueprints
from Websites.apis.routes import dashboard_data_blueprint

#import der Konfigurationsvariablen
from configs.config import isConfig_loaded, secret_key, debug_mode, email_password, jwt_secret_key

#Import der Datenbankklasse und gibt db eine Verbindung zur Datenbank
from data.student_database import DatabaseStudent

#Import der User Klasse
from utils.UserMixin import User

#Initialisierung der Datenbankverbindung
db = DatabaseStudent("student")

#Initialisierung des Login Managers
login_manager = LoginManager()


#Lädt den Benutzer basierend auf der Benutzer-ID
@login_manager.user_loader
def load_user(user_id):
    find_student = db.find_student_by_uuid(user_id)
    if find_student:
        return User(find_student)
    return None

#Hauptfunktion
def create_app(debug = debug_mode):
    #Erstellen der Flask App und Konfigurationen
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = secret_key
    app.config["JWT_SECRET_KEY"] = jwt_secret_key
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'schul.dashboard@gmail.com'
    app.config['MAIL_PASSWORD'] = email_password
    app.config['MAIL_DEFAULT_SENDER'] = 'schul.dashboard@gmail.com'
    
    #Initialisierung der Erweiterungen
    bcrypt.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    #einitialisierung des Login Managers
    login_manager.init_app(app)
    login_manager.login_view = "login.index"
    
    #Registrierung der Blueprints
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
    app.register_blueprint(page_not_found_blueprint, url_prefix="/page_not_found")
    app.register_blueprint(register_student_blueprint, url_prefix="/register_student")
    app.register_blueprint(login_blueprint, url_prefix="/login")
    app.register_blueprint(profile_blueprint, url_prefix="/profile")
    app.register_blueprint(codeconfirm_blueprint, url_prefix="/codeconfirm")
    app.register_blueprint(stundenplan_blueprint, url_prefix="/stundenplan")
    
    #Registrierung der Blueprints für API
    app.register_blueprint(dashboard_data_blueprint, url_prefix="/dashboard_data")
    app.register_blueprint(login_data_require_blueprint, url_prefix="/login_data")
    app.register_blueprint(register_data_require_blueprint, url_prefix="/register_data")
    app.register_blueprint(codeconfirm_data_require_blueprint, url_prefix="/codeconfirm_data")
    
    #Wenn keine Website gefunden wurde, ruft der Server diese Website auf.
    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for("page_not_found.index"))
    
    #Abmelden Route - Löscht die Session und leitet auf die Mainpage weiter
    @app.route("/logout/")
    @login_required
    def logout():
        session.clear() #cookies/session löschen
        logout_user() #Flask-Login Abmeldung
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