#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
dashboard_data_blueprint = Blueprint("dashboard_data", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes