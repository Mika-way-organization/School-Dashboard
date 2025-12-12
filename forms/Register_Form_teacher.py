"""Modul: Register_Form_teacher

Funktion: Dieses Modul definiert die Klasse `RegisterForm`, die zur Erfassung und umfassenden Validierung von Benutzerdaten (Benutzername, E-Mail und Passwort) während des Registrierungsprozesses dient.

Bestandteile:
1.  `username` (`StringField`): Feld zur Eingabe des Benutzernamens. Validiert auf Nicht-Leerheit und eine Länge zwischen 2 und 20 Zeichen.
2.  `email` (`StringField`): Feld zur Eingabe der E-Mail-Adresse. Validiert auf Nicht-Leerheit und gültiges E-Mail-Format.
3.  `password` (`PasswordField`): Feld zur Eingabe des Passworts. Validiert auf Nicht-Leerheit.
4.  `confirm_password` (`PasswordField`): Feld zur erneuten Eingabe des Passworts. Validiert auf Nicht-Leerheit und muss mit dem Wert des `password`-Feldes übereinstimmen (`EqualTo('password')`).
5.  `submit` (`SubmitField`): Schaltfläche zum Absenden (Registrieren) des Formulars.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

schools = [
    ('Keine Angabe', 'Keine Angabe'),
    ('Staatliche Berufsschule 2 - Aschaffenburg', 'Staatliche Berufsschule 2 - Aschaffenburg')
]

class RegisterForm(FlaskForm):
    selectfield = SelectField('Schule', choices=schools, validators=[DataRequired()])
    username = StringField('Benutzername', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Benutzername"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    first_name = StringField('Vorname', validators=[DataRequired(), Length(min=1, max=30)], render_kw={"placeholder": "Vorname (Optional)"})
    last_name = StringField('Nachname', validators=[DataRequired(), Length(min=1, max=30)], render_kw={"placeholder": "Nachname (Optional)"})
    password = PasswordField('Passwort', validators=[DataRequired(), Length(min=8, max=50)], render_kw={"placeholder": "Passwort"})
    confirm_password = PasswordField('Passwort bestätigen', validators=[DataRequired(), EqualTo('password', message='Passwörter müssen übereinstimmen')], render_kw={"placeholder": "Passwort bestätigen"})
    submit = SubmitField('Registrieren')