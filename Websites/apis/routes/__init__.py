#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
dashboard_data_blueprint = Blueprint("dashboard_data", __name__)
login_data_require_blueprint = Blueprint("login_data_require", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes