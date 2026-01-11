#Import Blueprint
from flask import Blueprint

#Blueprint erstellen
teacher_blueprint = Blueprint("teacherpanel", __name__, template_folder='templates', static_folder='static')

teacher_create_school_blueprint = Blueprint("teacher_create_school", __name__)

give_school_data_blueprint = Blueprint("give_school_data", __name__)

save_school_data_blueprint = Blueprint("save_school_data", __name__)

save_class_data_blueprint = Blueprint("save_class_data", __name__)

give_class_data_blueprint = Blueprint("give_class_data", __name__)

save_timetable_data_blueprint = Blueprint("save_timetable_data", __name__)

give_timetable_data_blueprint = Blueprint("give_timetable_data", __name__)

#Impotiert alles Wichtige von routes.py
from . import routes