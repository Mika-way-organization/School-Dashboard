#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
codeconfirm_blueprint = Blueprint("codeconfirm", __name__, template_folder='templates', static_folder='static')

#Impotiert alles Wichtige von routes.py
from . import routes