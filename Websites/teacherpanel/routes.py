#Import Flask
from flask import render_template, redirect, url_for, request, jsonify
from . import teacher_blueprint, teacher_create_school_blueprint, give_school_data_blueprint, save_school_data_blueprint, save_class_data_blueprint, give_class_data_blueprint, save_timetable_data_blueprint, give_timetable_data_blueprint
from flask_login import current_user

from utils.uuid_generator import generate_uuid

from data.student_database import DatabaseStudent
from data.teacher_database import DatabaseTeacher
from data.school_database import DatabaseSchool
from data.admin_database import DatabaseAdmin
from data.class_database import DatabaseClasses
from data.timetable_database import DatabaseTimetable

studentd_db = DatabaseStudent("student")
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

#school routes ----------------------------------------------------------------------------------------------------------

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

#class routes ----------------------------------------------------------------------------------------------------------

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
    classStudents = data.get('classStudents')

    classStudents_id = []
    
    for student in classStudents:
        # 2. Daten abrufen
        student_data = studentd_db.find_student_by_name(student)
        
        # 3. Sicherheitscheck: Wurde der Schüler gefunden?
        if student_data and "uuid" in student_data:
            student_id = student_data["uuid"]
            # 4. Mit append() zur Liste hinzufügen
            classStudents_id.append(student_id)
        else:
            # Optional: Logging, falls ein Name im JSON falsch war
            print(f"Warnung: Schüler '{student}' nicht in der Datenbank gefunden.")

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
        students=classStudents_id if classStudents_id else [],
    )

    for student in classStudents:
        student_data = studentd_db.find_student_by_name(student)
        if student_data:
            studentd_db.update_student_data(student_data["uuid"], {
                "classData": {
                    "classID": class_uuid,
                    "gradeLevel": classGrade,
                    "section": classGroupe,
                    "classTeacherId": teacher_uuid,
                }
            })
        else:
            return jsonify({"status": "error", "message": f"Schüler {student} nicht gefunden."}), 404

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

    student_name_list = []
    for student_id in class_data["students"]:
        student = studentd_db.find_student_by_uuid(student_id)
        if student:
            student_name_list.append(student["username"])
        else:
            student_name_list.append("Unbekannt")

    class_info = {
        "className": class_data["className"],
        "classGrade": class_data["gradeLevel"],
        "classGroupe": class_data["section"],
        "classRoom": class_data["classRoom"],
        "classTeacher": teacher_name,
        "classStudent": student_name_list,
    }

    return jsonify({"status": "success", "class_data": class_info}), 200

@give_class_data_blueprint.route('/students', methods=['GET'])
def give_class_students():
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
        print("Klasse nicht gefunden.")
    
    students = studentd_db.give_all_students_username()

    print(students)
    
    if not students:
        return jsonify({"status": "error", "message": "Keine Schüler in der Klasse gefunden."}), 404

    return jsonify({"status": "success", "students": students}), 200
    
    
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

#timetable routes ----------------------------------------------------------------------------------------------------------

@save_timetable_data_blueprint.route('/require', methods=['POST'])
def save_timetable_data():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400

    teacher = teacher_db.find_teacher_by_uuid(current_user.id)

    if not teacher:
        return jsonify({"status": "error", "message": "Benuter nicht gefundne."}), 404

    school_uuid = teacher["school_uuid"]

    school = school_db.find_school_by_uuid(school_uuid)

    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    class_id = school["classes"][-1] if school["classes"] else False

    if not class_id:
        return jsonify({"status": "error", "message": "Keine Klasse gefunden."}), 404
    
    Class = class_db.find_class_by_uuid(class_id)

    if not Class:
        return jsonify({"status": "error", "message": "Klasse nicht gefunden."}), 404
    
    scheduleSubject = data.get('scheduleSubject')
    scheduleTeacher = data.get('scheduleTeacher')
    scheduleDay = data.get('scheduleDay')
    scheduleDate = data.get('scheduleDay')
    schedulelesson_hour = data.get('lessonHour')
    scheduleRoom = data.get('scheduleRoom')
    scheduleHomework = data.get('scheduleHomework')
    scheduleNotes = data.get('scheduleNotes')

    if not scheduleSubject or not scheduleTeacher or not scheduleDay or not scheduleDate or not schedulelesson_hour or not scheduleRoom:
        return jsonify({"status": "error", "message": "Alle Pflichtfelder müssen ausgefüllt sein."}), 400

    find_timetable = timetable_db.find_timetable_by_class_and_date(
        class_id=Class["uuid"],
        date=scheduleDate
    )



    if not find_timetable:
        timetable_id = generate_uuid()
        timetable_data = timetable_db.timetable_formular(
            uuid=timetable_id,
            class_id=Class["uuid"],
            date=scheduleDate
        )
        timetable_db.create_timetable(timetable_data)
        
        class_data = class_db.find_class_by_uuid(class_id)

        timeable_list = class_data.get("timetableID", [])
        timeable_list.append(timetable_id)
        
        #Update der Klassendaten mit der Stundenplan ID
        class_db.update_class_data(class_id, {
        "timetableID": timeable_list
        })
    
    timetable_db.add_schedule_entry(
        class_id=Class["uuid"],
        date=scheduleDate,
        subject=scheduleSubject,
        teacher=scheduleTeacher,
        room=scheduleRoom,
        note=scheduleNotes,
        homework=scheduleHomework,
        lesson_hour=schedulelesson_hour
    )

    return jsonify({"status": "success", "message": "Stundenplandaten erfolgreich gespeichert."}), 201

@give_timetable_data_blueprint.route('/data', methods=['GET', 'POST'])
def give_timetable_data():
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "Nicht authentifiziert."}), 401
    
    teacher = teacher_db.find_teacher_by_uuid(current_user.id)

    if not teacher:
        return jsonify({"status": "error", "message": "Benuter nicht gefundne."}), 404

    school_uuid = teacher["school_uuid"]

    school = school_db.find_school_by_uuid(school_uuid)

    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    class_id = school["classes"][-1] if school["classes"] else False

    if not class_id:
        return jsonify({"status": "error", "message": "Keine Klasse gefunden."}), 404
    
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400

    timetable = timetable_db.find_timetable_by_class_and_date_and_hour(
        class_id=class_id,
        date=data.get('date'),
        lesson_hour=data.get('hour')
        )
    
    if timetable is None:
        return jsonify({"status": "miss", "message": "Stundenplandaten nicht gefunden."}), 404
    else:

        timetable_data = {
            "scheduleSubject": timetable.get("subject"),
            "scheduleTeacher": timetable.get("teacher"),
            "scheduleDay": data.get('date'),
            "schedulelessenHour": timetable.get("lesson_hour"),
            "scheduleRoom": timetable.get("room"),
            "scheduleHomework": timetable.get("homework"),
            "scheduleNotes": timetable.get("note"),
        }

        return jsonify({"status": "success", "data": timetable_data}), 200

@save_timetable_data_blueprint.route('/update', methods=['POST'])
def save_timetable():
    data = request.get_json()
    
    if not data:
        return jsonify({"status": "error", "message": "Ungültige Anfrage."}), 400

    teacher = teacher_db.find_teacher_by_uuid(current_user.id)

    if not teacher:
        return jsonify({"status": "error", "message": "Benuter nicht gefundne."}), 404

    school_uuid = teacher["school_uuid"]

    school = school_db.find_school_by_uuid(school_uuid)

    if not school:
        return jsonify({"status": "error", "message": "Schule nicht gefunden."}), 404
    
    class_id = school["classes"][-1] if school["classes"] else False

    if not class_id:
        return jsonify({"status": "error", "message": "Keine Klasse gefunden."}), 404
    
    Class = class_db.find_class_by_uuid(class_id)

    if not Class:
        return jsonify({"status": "error", "message": "Klasse nicht gefunden."}), 404
    
    scheduleSubject = data.get('scheduleSubject')
    scheduleTeacher = data.get('scheduleTeacher')
    scheduleDay = data.get('scheduleDay')
    scheduleDate = data.get('scheduleDay')
    schedulelesson_hour = data.get('lessonHour')
    scheduleRoom = data.get('scheduleRoom')
    scheduleHomework = data.get('scheduleHomework')
    scheduleNotes = data.get('scheduleNotes')

    if not scheduleSubject or not scheduleTeacher or not scheduleDay or not scheduleDate or not schedulelesson_hour or not scheduleRoom:
        return jsonify({"status": "error", "message": "Alle Pflichtfelder müssen ausgefüllt sein."}), 400

    find_fimtable = timetable_db.find_timetable_by_class_and_date_and_hour(
        class_id=Class["uuid"],
        date=scheduleDate,
        lesson_hour=schedulelesson_hour
    )
    
    if find_fimtable:
        timetable_db.update_schedule_entry(
            class_id=Class["uuid"],
            date=scheduleDate,
            lesson_hour=schedulelesson_hour,
            subject=scheduleSubject,
            teacher=scheduleTeacher,
            room=scheduleRoom,
            note=scheduleNotes,
            homework=scheduleHomework
        )
        return jsonify({"status": "success", "message": "Stundenplandaten erfolgreich aktualisiert."}), 201
    else:
        return jsonify({"status": "error", "message": "Unterrichtsstunde nicht gefunden."}), 404