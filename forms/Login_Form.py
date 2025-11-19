"""Modul: Login_Form

Funktion: Dieses Modul definiert die Klasse `LoginForm`, die zur Erfassung und Validierung von Benutzer-Anmeldedaten (E-Mail und Passwort) im Rahmen der Webanwendung dient.

Bestandteile:
1.  `email` (`StringField`): Feld zur Eingabe der E-Mail-Adresse, validiert auf Korrektheit.
2.  `password` (`PasswordField`): Feld zur Eingabe des Passworts, validiert auf Nicht-Leerheit.
3.  `submit` (`SubmitField`): Schaltfläche zum Absenden (Anmelden) des Formulars.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Passwort', validators=[DataRequired()], render_kw={"placeholder": "Passwort"})
    submit = SubmitField('Anmelden')