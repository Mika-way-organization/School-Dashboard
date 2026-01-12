#Import Flask
from flask import render_template, redirect, url_for, request, jsonify
from . import teacher_blueprint, teacher_create_school_blueprint, give_school_data_blueprint, save_school_data_blueprint, save_class_data_blueprint, give_class_data_blueprint, save_timetable_data_blueprint, give_timetable_data_blueprint
from flask_login import current_user

from utils.uuid_generator import generate_uuid

from data.teacher_database import DatabaseTeacher
from data.school_database import DatabaseSchool
from data.admin_database import DatabaseAdmin
from data.class_database import DatabaseClasses
from data.timetable_database import DatabaseTimetable

teacher_db = DatabaseTeacher("teacher")
school_db = DatabaseSchool("school")
admin_db = DatabaseAdmin("admin")
class_db = DatabaseClasses("class")
timetable_db = DatabaseTimetable("timetable")

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

#Diese API speichert die aktualisierten Schuldaten in die MongoDB
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

@save_class_data_blueprint.route('/require', methods=['POST'])
def get_class_school_data():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400

    className = data.get('className')
    classGrade = data.get('classGrade')
    classGroupe = data.get('classGroupe')
    classRoom = data.get('classRoom')
    classTeacher = data.get('classTeacher')
    classStudent = data.get('classStudent')

    teacher = teacher_db.find_teacher_by_name(classTeacher)

    find_teacher = teacher_db.find_teacher_by_uuid(current_user.id)
    find_admin = admin_db.find_admin_by_uuid(current_user.id)

    if not find_teacher and not find_admin:
        return jsonify({"status": "error", "message": "Du hast keine Berechtigung, eine Klasse zu erstellen."}), 404

    if not teacher:
        return jsonify({"status": "error", "message": "Lehrer nicht gefunden."}), 404

    if not className or not classGrade or not classGroupe or not classRoom or not classTeacher:
        return jsonify({"status": "error", "message": "Alle Felder müssen ausgefüllt sein."}), 400
    
    school_uuid = teacher["school_uuid"]

    school = school_db.find_school_by_uuid(school_uuid)

    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404

    teacher_uuid = teacher["uuid"]

    class_uuid = generate_uuid()
    class_format = class_db.class_formular(
        uuid=class_uuid,
        class_name=className,
        grade_level=classGrade,
        section=classGroupe,
        school_id=school_uuid,
        class_teacher_id=teacher_uuid,
        classRoom=classRoom,
        students=classStudent if classStudent else [],
    )

    school_db.update_school_data(school_uuid, {
        "classes": school["classes"] + [class_uuid]
    })
    
    class_db.create_class(class_format)
    return jsonify({"status": "success", "message": "Klasse erfolgreich erstellt."}), 201

@give_class_data_blueprint.route('/data', methods=['GET'])
def give_class_data():
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Nicht authentifiziert."}), 401
    
    teacher = teacher_db.find_teacher_by_uuid(current_user.id)

    if not teacher:
        return jsonify({"status": "error", "message": "Benuter nicht gefundne."}), 404
    

    school_uuid = teacher["school_uuid"]

    school = school_db.find_school_by_uuid(school_uuid)

    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    class_uuid = school["classes"][-1] if school["classes"] else None

    class_data = class_db.find_class_by_uuid(class_uuid)

    if not class_data:
        return jsonify({"status": "error", "message": "Klasse nicht gefunden."}), 404
    
    teacher_id = class_data["classTeacherId"]
    teacher = teacher_db.find_teacher_by_uuid(teacher_id)
    teacher_name = teacher["username"] if teacher else "Unbekannt"

    class_info = {
        "className": class_data["className"],
        "classGrade": class_data["gradeLevel"],
        "classGroupe": class_data["section"],
        "classRoom": class_data["classRoom"],
        "classTeacher": teacher_name,
        "classStudent": class_data["students"],
    }

    return jsonify({"status": "success", "class_data": class_info}), 200
    
    
    
@save_class_data_blueprint.route('/save', methods=['POST'])
def save_class_data():
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Nicht authentifiziert."}), 401
    
    teacher = teacher_db.find_teacher_by_uuid(current_user.id)
    
    if not teacher:
        return jsonify({"status": "error", "message": "Benutzer nicht gefunden."}), 404
    
    school_uuid = teacher["school_uuid"]
    
    school = school_db.find_school_by_uuid(school_uuid)
    
    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    teacher_name = teacher["username"]
    find_teacher = teacher_db.find_teacher_by_name(teacher_name)
    if not find_teacher:
        return jsonify({"status": "error", "message": "Lehrer nicht gefunden."}), 404

    # Diese Variable sollte noch überarbeitet werden.
    class_id = school["classes"][-1] if school["classes"] else None

    if not class_id:
        return jsonify({"status": "error", "message": "Keine Klasse zum Aktualisieren gefunden."}), 404

    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400
    
    class_update_data = {
        "className": data.get('className'),
        "gradeLevel": data.get('classGrade'),
        "section": data.get('classGroupe'),
        "classRoom": data.get('classRoom'),
        "classTeacher": data.get('classTeacher'),
        "students": data.get('classStudent', []),
    }

    class_db.update_class_data(class_id, class_update_data)
    
    return jsonify({"status": "success", "message": "Klassendaten erfolgreich aktualisiert."}), 200

@save_timetable_data_blueprint.route('/require', methods=['POST'])
def save_timetable_data():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400

    teacher = teacher_db.find_teacher_by_uuid(current_user.id)

    if not teacher:
        return jsonify({"status": "error", "message": "Benutzer nicht gefunden."}), 404
    

    scheduleSubject = data.get('scheduleSubject')
    scheduleTeacher = data.get('scheduleTeacher')
    scheduleDay = data.get('scheduleDay')
    scheduleDate = data.get('scheduleDate')
    scheduleStartTime = data.get('scheduleStartTime')
    scheduleEndTime = data.get('scheduleEndTime')
    scheduleRoom = data.get('scheduleRoom')
    scheduleHomework = data.get('scheduleHomework')
    scheduleNotes = data.get('scheduleNotes')

    if not scheduleSubject or not scheduleTeacher or not scheduleDay or not scheduleDate or not scheduleStartTime or not scheduleEndTime or not scheduleRoom:
        return jsonify({"status": "error", "message": "Alle Pflichtfelder müssen ausgefüllt sein."}), 400

    timetable_data = timetable_db.timetable_formular(
        uuid=generate_uuid(),
        class_id=teacher["school_uuid"],
        week_days={
            scheduleDay: [
                timetable_db.timetable_period_formular(
                    subject=scheduleSubject,
                    teacher=scheduleTeacher,
                    note=scheduleNotes,
                    homework=scheduleHomework,
                    start_time=scheduleStartTime,
                    end_time=scheduleEndTime,
                )
            ]
        }
    )

    return jsonify({"status": "success", "message": "Stundenplandaten erfolgreich gespeichert."}), 200