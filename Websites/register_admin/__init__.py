#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
register_admin_blueprint = Blueprint("register_admin", __name__, template_folder='templates', static_folder='static')
admin_register_data_require_blueprint = Blueprint("register_admin_data_require", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes