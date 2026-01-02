#Import Flask
from flask import render_template, redirect, url_for, request, jsonify
from . import teacher_blueprint, teacher_create_school_blueprint, give_school_data_blueprint, save_school_data_blueprint
from flask_login import current_user

from utils.uuid_generator import generate_uuid

from data.teacher_database import DatabaseTeacher
from data.school_database import DatabaseSchool
from data.admin_database import DatabaseAdmin

teacher_db = DatabaseTeacher("teacher")
school_db = DatabaseSchool("school")
admin_db = DatabaseAdmin("admin")

#Erstellt die Verbindung zur HTML Datei her
@teacher_blueprint.route('/<user_id>')
def index(user_id):
    #Überprüft, ob der Benutzer angemeldet ist
    if current_user.is_authenticated:
        username = current_user.username
        role = current_user.role
        
        #Stellt sicher, dass der Benutzer nur auf sein eigenes Profil zugreifen kann
        if current_user.id != user_id:
            return redirect(url_for('teacherpanel.index', user_id=current_user.id))
        
        teacher = teacher_db.find_teacher_by_uuid(user_id)
        
        #Wenn der Benutzer nicht gefunden wird, leite zurück zum Dashboard
        if not teacher:
            return redirect(url_for('dashboard.index'))
        
    else:
        return redirect(url_for('login.index'))
        
    return render_template('teacherpanel.html',
                           username=username, 
                           role=role)
    
@teacher_create_school_blueprint.route('/require', methods=['POST'])
def create_school():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400
    
    schoolName = data.get('schoolName')
    email = data.get('email')
    tel = data.get('phone')
    plz = data.get('postalcode')
    city = data.get('city')
    housnumber = data.get('housenumber')
    street = data.get('street')
    state = data.get('state')
    country = data.get('country')
    
    find_school_name = school_db.find_school_by_name(schoolName)
    find_school = school_db.find_school_by_email(email)
    
    find_teacher = teacher_db.find_teacher_by_uuid(current_user.id)
    find_admin = admin_db.find_admin_by_uuid(current_user.id)
    
    if not find_teacher and not find_admin:
        return jsonify({"status": "error", "message": "Du hast keine Berechtigung, eine Schule zu erstellen."}), 404
    
    if find_school:
        return jsonify({"status": "error", "message": "Eine Schule mit dieser E-Mail existiert bereits."}), 409
    
    if find_school_name:
        return jsonify({"status": "error", "message": "Eine Schule mit diesem Namen existiert bereits."}), 409
    
    if not schoolName or not email or not tel or not plz or not city or not street or not state or not country or not housnumber:
        return jsonify({"status": "error", "message": "Alle Felder müssen ausgefüllt sein."}), 400
    
    if not find_school and not find_school_name:
        school_uuid = generate_uuid()
        
        school_fomrmat = school_db.school_formular(
            uuid=school_uuid,
            school_name=schoolName,
            street=street,
            house_number=housnumber,
            city=city,
            state=state,
            zip_code=plz,
            country=country,
            emails=[email],
            phone_numbers=[tel],
            school_leader=current_user.id,
            upgradeBy=current_user.id
            
        )
        school_db.create_school(school_fomrmat)

        teacher_db.update_teacher_data(current_user.id, {
            "school_uuid": school_uuid
            })
        
        return jsonify({"status": "success", "message": "Schule erfolgreich erstellt."}), 201
    else:
        return jsonify({"status": "error", "message": "Die Schule ist schon vorhanden."}), 500

# Für Admin wird noch eine weitere Funktion benötigt, um die Schuldaten abzurufen.

#Diese API gibt die Schuldaten die vom Lehrerprofil verlinkt ist zurück und speichert diese in die MongoDB
@give_school_data_blueprint.route('/data', methods=['GET'])
def give_school_data():
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Nicht authentifiziert."}), 401
    
    teacher = teacher_db.find_teacher_by_uuid(current_user.id)
    
    if not teacher:
        return jsonify({"status": "error", "message": "Benutzer nicht gefunden."}), 404
    
    school_uuid = teacher["school_uuid"]

    if teacher:
        school = school_db.find_school_by_uuid(school_uuid)
    
    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    school_data = {
        "schoolName": school["schoolName"],
        "address": school["address"],
        "phoneNumbers": school["phoneNumbers"],
        "emails": school["emails"],
        "schoolMembers": school["schoolMembers"],
        "classes": school["classes"],
        }
    
    return jsonify({"status": "success", "school_data": school_data}), 200
    
@save_school_data_blueprint.route('/save', methods=['POST'])
def save_school_data():
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Nicht authentifiziert."}), 401
    
    teacher = teacher_db.find_teacher_by_uuid(current_user.id)
    
    if not teacher:
        return jsonify({"status": "error", "message": "Benutzer nicht gefunden."}), 404
    
    school_uuid = teacher["school_uuid"]
    
    school = school_db.find_school_by_uuid(school_uuid)
    
    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400
    
    schoolName = data.get('schoolName')
    email = data.get('email')
    tel = data.get('phone')
    plz = data.get('postalcode')
    city = data.get('city')
    housnumber = data.get('housenumber')
    street = data.get('street')
    state = data.get('state')
    country = data.get('country')
    
    if not schoolName or not email or not tel or not plz or not city or not street or not state or not country or not housnumber:
        return jsonify({"status": "error", "message": "Alle Felder müssen ausgefüllt sein."}), 400
    
    updated_data = {
        "schoolName": schoolName,
        "address": {
            "street": street,
            "houseNumber": housnumber,
            "city": city,
            "state": state,
            "zipCode": plz,
            "country": country
        },
        "emails": [email],
        "phoneNumbers": [tel]
    }
    
    school_db.update_school_data(school_uuid, updated_data)
    
    return jsonify({"status": "success", "message": "Schuldaten erfolgreich aktualisiert."}), 200