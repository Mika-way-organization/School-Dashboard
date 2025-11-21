#Import Flask
from flask import render_template
from . import register_student_blueprint

#Erstellt die Verbindung zur HTML Datei her
@register_student_blueprint.route('/')
def index():
    return render_template('register_student.html')