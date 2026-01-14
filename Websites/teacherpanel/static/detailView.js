//Funktionenaus andere Dateien importieren
import { create_school_submit } from './create_school_function.js';
import { update_school_submit } from './update_school_function.js';

import { create_class_submit } from './create_class.js';
import { update_class_submit } from './update_class.js';

import { create_timetable_submit, date_event_listener } from './timetable.js';

// Detail Ansicht Elemente
const detailView = document.getElementById('detailView');
const detailInhalt = document.getElementById('detail_inhalt');
const underlayDetail = document.getElementById('underlay_detail');
const closeButton = document.getElementById('closeButton');

const button_Schule_erstellen = document.getElementById('Schule_erstellen');
const button_Schule_bearbeiten = document.getElementById('Schule_bearbeiten');
const button_Klasse_erstellen = document.getElementById('Klasse_erstellen');
const button_Klasse_bearbeiten = document.getElementById('Klasse_bearbeiten');
const button_Stundenplan = document.getElementById('Stundenplan');

function closeDetailView() {
    detailView.style.display = 'none';
    underlayDetail.style.display = 'none';

    setTimeout(() => {
        underlayDetail.style.opacity = '0';
        detailView.style.opacity = '0';
    });

    detailInhalt.innerHTML = '';
}

function openDetailView() {
    detailView.style.display = 'block';
    underlayDetail.style.display = 'block';
    
    setTimeout(() => {
        detailView.style.opacity = '1';
        underlayDetail.style.opacity = '1';
    });
}

/*
Warum hier kein Escape Key down gemacht wird oder das man auch auf den Underlay klicken kann um die Detailansicht zu schließen?

Weil wenn man sich verclickt und die Detailansicht schließt, dann sind alle Eingaben weg. Um dies zu verhindern,muss der Nutzer explizit auf den Schließen Button klicken.
*/

/*Bisher sind alle nur Beispiel Daten, diese müssen noch mit den echten Daten verbunden werden.*/

/**** Inhalt/Formen der Detailansicht *****/

/* Schule erstellen Formular */
function setDetailInhalt_CreateSchool() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3 id="createSchoolTitle">Schule erstellen</h3>
        <hr>
        <form id="createSchoolForm">
            <div class="form-group">
                <label for="schoolName">Name</label>
                <input type="text" id="schoolName" name="schoolName" required>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="schoolEmail">E-Mail</label>
                    <input type="email" id="schoolEmail" name="schoolEmail" required>
                </div>
                <div class="form-group">
                    <label for="schoolPhone">Telefonnummer</label>
                    <input type="tel" id="schoolPhone" name="schoolPhone" required>
                </div>
            </div>

            <hr>
            <h4>Adresse der Schule:</h4>

            <div class="form-row">
                <div class="form-group zip-code">
                    <label for="schoolpostalcode">PLZ</label>
                    <input type="text" id="schoolpostalcode" name="schoolpostalcode" required>
                </div>
                <div class="form-group">
                    <label for="schoolcity">Stadt</label>
                    <input type="text" id="schoolcity" name="schoolcity" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="schoolstreet">Straße</label>
                    <input type="text" id="schoolstreet" name="schoolstreet" required>
                </div>
                <div class="form-goup">
                    <label for="schoolhouseNumber">Hausnummer</label>
                    <input type="text" id="schoolhouseNumber" name="schoolhouseNumber" required>
                </div>
                <div class="form-goup">
                    <label for="schoolstate">Bundesland</label>
                    <input type="text" id="schoolstate" name="schoolstate">
                </div>
                <div class="form-group">
                    <label for="schoolcountry">Land</label>
                    <input type="text" id="schoolcountry" name="schoolcountry" required>
                </div>
            </div>

            <button type="submit" class="custom-btn" id="createSchoolButton">Erstellen</button>
        </form>
    `;
    create_school_submit();
}

function setDetailInhalt_ConfigureSchool() {
    openDetailView();
    // Die Daten abrufen
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/give_school_data/data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(async response => {
        const text = await response.text();
        let data;
        console.log(text);
        try {
            data = JSON.parse(text);
        } catch (err) {
            console.error("Fehler beim Parsen von JSON:", err);
            throw err;
        }
        return data;
    })
      .then(data => {
          console.log(data);
          if (data.status === "success") {
            let schoolData = data.school_data;

            detailInhalt.innerHTML = `
                <h3 id="configureSchoolTitle">Schule bearbeiten</h3>
                <hr>
                <form id="configureSchoolForm">
                    <div class="form-group">
                        <label for="schoolName">Name</label>
                        <input type="text" id="schoolName" name="schoolName" value="${schoolData.schoolName}" required>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="schoolEmail">E-Mail</label>
                            <input type="email" id="schoolEmail" name="schoolEmail" value="${schoolData.emails}" required>
                        </div>
                        <div class="form-group">
                            <label for="schoolPhone">Telefonnummer</label>
                            <input type="tel" id="schoolPhone" name="schoolPhone" value="${schoolData.phoneNumbers}" required>
                        </div>
                    </div>

                    <hr>
                    <h4>Adresse der Schule:</h4>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="schoolpostalcode">PLZ</label>
                            <input type="text" id="schoolpostalcode" name="schoolpostalcode" value="${schoolData.address.zipCode}" required>
                        </div>
                        <div class="form-group">
                            <label for="schoolcity">Stadt</label>
                            <input type="text" id="schoolcity" name="schoolcity" value="${schoolData.address.city}" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="schoolstreet">Straße</label>
                            <input type="text" id="schoolstreet" name="schoolstreet" value="${schoolData.address.street}" required>
                        </div>
                        <div class="form-goup">
                            <label for="schoolhouseNumber">Hausnummer</label>
                            <input type="text" id="schoolhouseNumber" name="schoolhouseNumber" value="${schoolData.address.houseNumber}" required>
                        </div>
                        <div class="form-goup">
                            <label for="schoolstate">Bundesland</label>
                            <input type="text" id="schoolstate" name="schoolstate" value="${schoolData.address.state}">
                        </div>
                        <div class="form-group">
                            <label for="schoolcountry">Land</label>
                            <input type="text" id="schoolcountry" name="schoolcountry" value="${schoolData.address.country}" required>
                        </div>
                    </div>

                    <button type="submit" class="custom-btn">Erstellen</button>
                </form>
            `;
            update_school_submit();
          } else {
              alert(body.message || 'Ein unbekannter Fehler ist aufgetreten beim Laden der Schuldaten.');
          }
      })
      .catch(error => {
          console.error("Fehler beim Abrufen der Daten:", error);
          alert('Es gab einen Fehler beim Abrufen der Schuldaten.');
    });
}

/*Klasse erstellen Formular */

function setDetailInhalt_CreateClass() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3 id="createClassTitle">Klasse erstellen</h3>
        <hr>
        <form id="createClassForm">
            <div class="form-row">
                <div class="form-group">
                    <label for="className">Name der Klasse:</label><br>
                    <input type="text" id="className" name="className" required><br><br>
                </div>
                <div class="form-group">
                    <label for="classGrade">Klassenstufe:</label><br>
                    <input type="number" id="classGrade" name="classGrade" required><br><br>
                </div>
                <div class="form-group">
                    <label for="classTeacher">Klassengruppe:</label><br>
                    <input type="text" id="classGroupe" name="classGroupe" required><br><br>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="classRoom">Klassenzimmer:</label><br>
                    <input type="text" id="classRoom" name="classRoom" required><br><br>
                </div>
                <div class="form-group">
                    <label for="classTeacher">Klassenlehrer:</label><br>
                    <input type="text" id="classTeacher" name="classTeacher" required><br><br>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="classStudent">Schüler (optional):</label><br>
                    <input type="text" id="classStudent" name="classStudent"><br><br>
                </div>
            </div>
            <button type="submit" class="custom-btn" id="createClassButton">Erstellen</button>
        </form>
    `
    create_class_submit();
}

function setDetailInhalt_ConfigureClass() {
    openDetailView();
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');    
    fetch('/give_class_data/data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    }).then(async response => {
        const text = await response.text();
        let data;
        console.log(text);
        try {
            data = JSON.parse(text);
        } catch (err) {
            console.error("Fehler beim Parsen von JSON:", err);
            throw err;
        }
        return data;
    }).then(data => {
        console.log(data);
        if (data.status === "success") {
            let classData = data.class_data;

            detailInhalt.innerHTML = `
                <h3 id="configureClassTitle">Klasse bearbeiten</h3>
                <hr>
                <form id="configureClassForm">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="className">Name der Klasse:</label><br>
                            <input type="text" id="className" name="className" value="${classData.className}" required><br><br>
                        </div>
                        <div class="form-group">
                            <label for="classGrade">Klassenstufe:</label><br>
                            <input type="number" id="classGrade" name="classGrade" value="${classData.classGrade}" required><br><br>
                        </div>
                        <div class="form-group">
                            <label for="classTeacher">Klassengruppe:</label><br>
                            <input type="text" id="classGroupe" name="classGroupe" value="${classData.classGroupe}" required><br><br>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="classRoom">Klassenzimmer:</label><br>
                            <input type="text" id="classRoom" name="classRoom" value="${classData.classRoom}" required><br><br>
                        </div>
                        <div class="form-group">
                            <label for="classTeacher">Klassenlehrer:</label><br>
                            <input type="text" id="classTeacher" name="classTeacher" value="${classData.classTeacher}" required><br><br>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="classStudent">Schüler</label><br>
                            <input type="text" id="classStudent" name="classStudent" value="${classData.classStudent}"><br><br>
                        </div>
                    </div>
                    <button type="submit" class="custom-btn" id="configureClassButton">Erstellen</button>
                </form>
            `;
            update_class_submit();
        } else {
            alert(body.message || 'Ein unbekannter Fehler ist aufgetreten beim Laden der Klassendaten.');
        }
    })
    .catch(error => {
        console.error("Fehler beim Abrufen der Daten:", error);
        alert('Es gab einen Fehler beim Abrufen der Klassendaten.', error);
    });
}

/*Stundenplan erstellen Formular */

function setDetailInhalt_Schedule() {
    openDetailView();
    detailInhalt.innerHTML = `
    <div style="display: flex; align-items: center; justify-content:建设; margin-bottom: 15px;">
            <div style="flex: 1; display: flex; justify-content: flex-start;">
                <input type="date" id="selectedDate" name="selectedDate">
            </div>

            <div style="flex: 2; text-align: center;">
                <h3 style="margin: 0;" id="scheduleTitle">Stundenplan</h3>
            </div>

            <div style="flex: 1;"></div>
        </div>
        <hr>
        <form id="ScheduleForm">
            <div class="form-row">
                <div class="form-group">
                    <label for="scheduleSubject">Fach des Stundenplans:</label><br>
                    <input type="text" id="scheduleSubject" name="scheduleSubject" required><br><br>
                </div>
                <div class="form-group">
                    <label for="scheduleTeacher">Lehrer des Stundenplans:</label><br>
                    <input type="text" id="scheduleTeacher" name="scheduleTeacher" required><br><br>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="lessonHour">Untterichtsstunde:</label><br>
                    <input type="number" id="lessonHour" name="lessonHour" required><br><br>
                </div>
                <div class="form-group">
                    <label for="scheduleRoom">Raum:</label><br>
                    <input type="text" id="scheduleRoom" name="scheduleRoom" required><br><br>
                </div>
            </div>
            <div class="form-group">
                <label for="scheduleHomework">Hausaufgaben (optional):</label><br>
                <textarea id="scheduleHomework" name="scheduleHomework"></textarea><br><br>
            </div>
            <div class="form-group">
                <label for="scheduleNotes">Notizen (optional):</label><br>
                <textarea id="scheduleNotes" name="scheduleNotes"></textarea><br><br>
            </div>
            <button type="submit" class="custom-btn" id="ScheduleButton">Erstellen</button>
        </form>
    `;

    const dateInput = document.getElementById('selectedDate');
    dateInput.value = new Date().toISOString().split('T')[0];
    
    date_event_listener();
    create_timetable_submit();
}


/*Event Listener für die Buttons um die Detailansicht zu öffnen*/

button_Schule_erstellen.addEventListener('click', setDetailInhalt_CreateSchool);
button_Schule_bearbeiten.addEventListener('click', setDetailInhalt_ConfigureSchool);
button_Klasse_erstellen.addEventListener('click', setDetailInhalt_CreateClass);
button_Klasse_bearbeiten.addEventListener('click', setDetailInhalt_ConfigureClass);
button_Stundenplan.addEventListener('click', setDetailInhalt_Schedule);

/*Detailansicht schließen (Hier wird noch eine Logik hinzugefügt um bevor das schließen eine Frage angezeigt bekommen ob er wirklich schließen will)*/
closeButton.addEventListener('click', closeDetailView);