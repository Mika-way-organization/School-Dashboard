# Import Flask
from flask import render_template, redirect, url_for, request, session, jsonify
from flask_login import current_user
from . import codeconfirm_blueprint, codeconfirm_data_require_blueprint
from datetime import timezone

from utils.get_datetime import get_current_datetime_aware_utc, get_current_datetime

# Importiere das Formular
from forms.Verification_Form import VerificationForm

# Importiere die Datenbankklasse
from data.student_database import DatabaseStudent

db = DatabaseStudent("student")


# Erstellt die Verbindung zur HTML Datei her
@codeconfirm_blueprint.route("/", methods=["GET", "POST"])
def index():
    # Überprüft, ob der Benutzer bereits angemeldet ist
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = VerificationForm()

    return render_template("codeconfirm.html", form=form)

@codeconfirm_data_require_blueprint.route("/require", methods=["POST"])
def codeconfirm_require():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400
    
    uuid = session.get("uuid")
    if not uuid:
        return jsonify({"status": "error", "message": "Keine UUID in der Sitzung gefunden."}), 400
    
    student = db.find_student_by_uuid(uuid)
    if not student:
        return jsonify({"status": "error", "message": "Student nicht gefunden."}), 404
    
    if student["verification"]["is_verify"]:
        return jsonify({"status": "error", "message": "Konto ist bereits verifiziert."}), 400
    
    if student["verification"]["code"] is None:
        return jsonify({"status": "error", "message": "Kein Verifizierungscode gefunden."}), 400
    
    expires_at_naive = student["verification"]["expiresAt"]
    cexpires_at_aware = expires_at_naive.replace(tzinfo=timezone.utc)
    if cexpires_at_aware < get_current_datetime_aware_utc():
        return jsonify({"status": "error", "message": "Der Verifizierungscode ist abgelaufen."}), 400
    
    if student["verification"]["code"] == data.get("code"):
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
        return jsonify({"status": "success", "message": "Konto erfolgreich verifiziert."}), 200
    else:
        return jsonify({"status": "error", "message": "Falscher Verifizierungscode eingegeben."}), 400