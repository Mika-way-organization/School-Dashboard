#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
codeconfirm_blueprint = Blueprint("codeconfirm", __name__, template_folder='templates', static_folder='static')
codeconfirm_data_require_blueprint = Blueprint("codeconfirm_data_require", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes