#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
teacher_blueprint = Blueprint("teacherpanel", __name__, template_folder='templates', static_folder='static')

#Impotiert alles Wichtige von routes.py
from . import routes