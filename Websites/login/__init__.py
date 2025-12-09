#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
login_blueprint = Blueprint("login", __name__, template_folder='templates', static_folder='static')
login_data_require_blueprint = Blueprint("login_data_require", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes