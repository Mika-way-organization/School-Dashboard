"""Modul: Verification_Form

Funktion: Definiert das Formular für die Verifizierungscode-Eingabe während der Registrierung.

Bestandteile:
1. `code`: Ein Textfeld zur Eingabe des Verifizierungscodes, das eine Validierung erfordert.
2. `submit`: Ein Button zum Absenden des Formulars.

"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class VerificationForm(FlaskForm):
    code = StringField('Verifizierungscode', 
                       validators=[DataRequired('Bitte geben Sie den Code ein.')], 
                       description="Geben Sie den Verifizierungscode ein, den Sie per E-Mail erhalten haben.", 
                       render_kw={"placeholder": "Verifizierungscode"})
    submit = SubmitField('Code bestätigen')