"""Welcome

Dies hier ist unser School-Dashboard Projekt.
Die app.py dient als Einstiegspunkt unserer Anwendung, von wo aus die Website gestartet und alle Blueprints initialisiert werden.


"""

#Import Flask (Die Hauptfunktion)
from flask import Flask, redirect, url_for

#Import der Bluprints
from Websites.dashboard import dashboard_blueprint
from Websites.page_not_found import page_not_found_blueprint

#Hauptfunktion
def create_app(debug = True):
    app = Flask(__name__)
    app.debug = debug

    #Registrierung der Blueprints
    app.register_blueprint(dashboard_blueprint, url_prefix="/dashboard")
    app.register_blueprint(page_not_found_blueprint, url_prefix="/page_not_found")

    #Wenn keine Website gefunden wurde, ruft der Server diese Website auf.
    @app.errorhandler(404)
    def page_not_found(error):
        return redirect(url_for("page_not_found.index"))
    
    #Läd unser Dashboard (Mainpage)
    @app.route("/")
    def root_redirect():
        return redirect(url_for("dashboard.index"))
    
    return app

#Ausführen des Servers
if __name__ == "__main__":
    app = create_app()
    app.run()