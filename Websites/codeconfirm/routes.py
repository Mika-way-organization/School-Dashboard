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
from data.admin_database import DatabaseAdmin
from data.teacher_database import DatabaseTeacher

db = DatabaseStudent("student")
db_admin = DatabaseAdmin("admin")
db_teacher = DatabaseTeacher("teacher")


# Erstellt die Verbindung zur HTML Datei her
@codeconfirm_blueprint.route("/", methods=["GET", "POST"])
def index():
    # Überprüft, ob der Benutzer bereits angemeldet ist
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = VerificationForm()

    return render_template("codeconfirm.html", form=form)

# Verarbeitung der Verifizierungsanforderung
@codeconfirm_data_require_blueprint.route("/require", methods=["POST"])
def codeconfirm_require():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400
    
    uuid = session.get("uuid")
    admin_uuid = session.get("admin_uuid")
    teacher_uuid = session.get("teacher_uuid")
    if not uuid and not admin_uuid and not teacher_uuid:
        return jsonify({"status": "error", "message": "Keine UUID in der Sitzung gefunden."}), 400
    
    
    user = db.find_student_by_uuid(uuid)
    admin_user = db_admin.find_admin_by_uuid(admin_uuid)
    teacher_user = db_teacher.find_teacher_by_uuid(teacher_uuid)
    
    # Überprüft, ob der Benutzer existiert
    # Für den Normalen User (student)
    if user:    
        if user["verification"]["is_verify"]:
            return jsonify({"status": "error", "message": "Konto ist bereits verifiziert."}), 400
        
        if user["verification"]["code"] is None:
            return jsonify({"status": "error", "message": "Kein Verifizierungscode gefunden."}), 400
        
        expires_at_naive = user["verification"]["expiresAt"]
        cexpires_at_aware = expires_at_naive.replace(tzinfo=timezone.utc)
        if cexpires_at_aware < get_current_datetime_aware_utc():
            return jsonify({"status": "error", "message": "Der Verifizierungscode ist abgelaufen."}), 400
        
        if user["verification"]["code"] == data.get("code"):
            db.update_user_data(
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
    
    # Für den Admin User
    elif admin_user:
        if admin_user["verification"]["is_verify"]:
            return jsonify({"status": "error", "message": "Konto ist bereits verifiziert."}), 400
        
        if admin_user["verification"]["code"] is None:
            return jsonify({"status": "error", "message": "Kein Verifizierungscode gefunden."}), 400
        
        expires_at_naive = admin_user["verification"]["expiresAt"]
        cexpires_at_aware = expires_at_naive.replace(tzinfo=timezone.utc)
        if cexpires_at_aware < get_current_datetime_aware_utc():
            return jsonify({"status": "error", "message": "Der Verifizierungscode ist abgelaufen."}), 400
        
        if admin_user["verification"]["code"] == data.get("code"):
            db_admin.update_admin_data(
                admin_uuid,
                {
                    "verification.is_verify": True,
                    "verification.code": None,
                    "verification.expiresAt": None,
                    "verification.verifiedAt": get_current_datetime(),
                },
            )
            session.pop("admin_uuid")
            return jsonify({"status": "success", "message": "Konto erfolgreich verifiziert."}), 200
        else:
            return jsonify({"status": "error", "message": "Falscher Verifizierungscode eingegeben."}), 400
    # Für den Lehrer
    elif teacher_user:
        if teacher_user["verification"]["is_verify"]:
            return jsonify({"status": "error", "message": "Konto ist bereits verifiziert."}), 400
        
        if teacher_user["verification"]["code"] is None:
            return jsonify({"status": "error", "message": "Kein Verifizierungscode gefunden."}), 400
        
        expires_at_naive = teacher_user["verification"]["expiresAt"]
        cexpires_at_aware = expires_at_naive.replace(tzinfo=timezone.utc)
        if cexpires_at_aware < get_current_datetime_aware_utc():
            return jsonify({"status": "error", "message": "Der Verifizierungscode ist abgelaufen."}), 400
        
        if teacher_user["verification"]["code"] == data.get("code"):
            db_teacher.update_teacher_data(
                teacher_uuid,
                {
                    "verification.is_verify": True,
                    "verification.code": None,
                    "verification.expiresAt": None,
                    "verification.verifiedAt": get_current_datetime(),
                },
            )
            session.pop("teacher_uuid")
            return jsonify({"status": "success", "message": "Konto erfolgreich verifiziert."}), 200
        else:
            return jsonify({"status": "error", "message": "Falscher Verifizierungscode eingegeben."}), 400
    # Wenn es keinen Benutzer gibt
    else:
        return jsonify({"status": "error", "message": "Benutzer nicht gefunden."}), 400