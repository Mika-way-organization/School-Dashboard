#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
register_teacher_blueprint = Blueprint("register_teacher", __name__, template_folder='templates', static_folder='static')
register_teacher_data_require_blueprint = Blueprint("register_teacher_data_require", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes