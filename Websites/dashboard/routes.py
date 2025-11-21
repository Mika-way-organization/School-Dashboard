#Import Flask
from flask import render_template, session, redirect, url_for, jsonify, request
from . import dashboard_blueprint

#Erstellt die Verbindung zur HTML Datei her
@dashboard_blueprint.route('/')
def index():
    # Überprüft, ob der Benutzer eingeloggt ist und holt den Benutzernamen
    if session.get('user_uuid'):
        username = session['username']
    else:
        username = None # Standardmäßig kein Benutzername

    return render_template('dashboard.html', 
                           username = username)