# Import Flask
from flask import render_template, redirect, url_for, request, flash, session
from flask_login import current_user
from . import codeconfirm_blueprint
from datetime import timezone

from utils.get_datetime import get_current_datetime_aware_utc, get_current_datetime

# Importiere das Formular
from forms.Verification_Form import VerificationForm

# Importiere die Datenbankklasse
from data.database import DatabaseStudent

db = DatabaseStudent("student")


# Erstellt die Verbindung zur HTML Datei her
@codeconfirm_blueprint.route("/", methods=["GET", "POST"])
def index():
    # Überprüft, ob der Benutzer bereits angemeldet ist
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = VerificationForm()
    # Verarbeitet das Formular wenn es abgeschickt wurde
    if request.method == "POST" and form.validate_on_submit():
        # Holt die UUID aus der Session
        uuid = session.get("uuid")
        
        if not uuid:
            print("Ungültige Anfrage. Keine UUID angegeben.")
            return redirect(url_for("codeconfirm.index"))

        # Sucht den Studenten in der Datenbank anhand der UUID
        student = db.find_student_by_uuid(uuid)
        if not student:
            return redirect(url_for("register_student.index"))

        # Überprüft ob das Konto bereits verifiziert ist
        if student["verification"]["is_verify"]:
            print("Konto ist bereits verifiziert.")
            return redirect(url_for("login.index"))

        # Überprüft ob ein Verifizierungscode in der Datenbank vorhanden ist
        if student["verification"]["code"] is None:
            print("Kein Verifizierungscode gefunden.")
            return redirect(url_for("codeconfirm.index"))

        # Überprüft ob der Verifizierungscode abgelaufen ist
        expires_at_naive = student["verification"]["expiresAt"]
        cexpires_at_aware = expires_at_naive.replace(tzinfo=timezone.utc)
        if cexpires_at_aware < get_current_datetime_aware_utc():
            flash("Der Verifizierungscode ist abgelaufen.")
            return redirect(url_for("codeconfirm.index"))

        # Überprüft ob der eingegebene Code mit dem in der Datenbank übereinstimmt
        if student["verification"]["code"] == form.code.data:
            db.update_student_data(
                uuid,
                {
                    "verification.is_verify": True,
                    "verification.code": None,
                    "verification.expiresAt": None,
                    "verification.verifiedAt": get_current_datetime(),
                },
            )
            session.pop("uuid")
            print("Konto erfolgreich verifiziert.")
            return redirect(url_for("login.index"))
        else:
            print("Falscher Verifizierungscode eingegeben:", form.code.data)
            return redirect(url_for("codeconfirm.index"))

    return render_template("codeconfirm.html", form=form)
