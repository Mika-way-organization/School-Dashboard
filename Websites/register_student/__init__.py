#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
register_student_blueprint = Blueprint("register_student", __name__, template_folder='templates', static_folder='static')
register_data_require_blueprint = Blueprint("register_data_require", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes