//Funktionenaus andere Dateien importieren
import { create_school_submit } from './create_school_function.js';
import { update_school_submit } from './update_school_function.js';

// Detail Ansicht Elemente
const detailView = document.getElementById('detailView');
const detailInhalt = document.getElementById('detail_inhalt');
const underlayDetail = document.getElementById('underlay_detail');
const closeButton = document.getElementById('closeButton');

const button_Schule_erstellen = document.getElementById('Schule_erstellen');
const button_Schule_bearbeiten = document.getElementById('Schule_bearbeiten');
const button_Klasse_erstellen = document.getElementById('Klasse_erstellen');
const button_Klasse_bearbeiten = document.getElementById('Klasse_bearbeiten');
const button_Stundenplan_erstellen = document.getElementById('Stundenplan_erstellen');
const button_Stundenplan_bearbeiten = document.getElementById('Stundenplan_bearbeiten');

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
                        <div class="form-group zip-code">
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
        <h3>Klasse erstellen</h3>
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
            </div>
            <button type="submit" class="custom-btn" id="createClassButton">Erstellen</button>
        </form>
    `
    document.getElementById('createClassForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Hier kannst du die Logik zum Erstellen der Klasse hinzufügen

        closeDetailView();
    });
}

function setDetailInhalt_ConfigureClass() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3>Klasse bearbeiten</h3>
        <hr>
        <form id="configureClassForm">
            <label for="className">Name der Klasse:</label><br>
            <input type="text" id="className" name="className" value="Aktueller Klassenname" required><br><br>
            <label for="classGrade">Klassenstufe:</label><br>
            <input type="number" id="classGrade" name="classGrade" value="67" required><br><br>
            <label for="classTeacher">Klassenlehrer:</label><br>
            <input type="text" id="classTeacher" name="classTeacher" value="Aktueller Klassenlehrer" required><br><br>
            <label for="classRoom">Klassenzimmer:</label><br>
            <input type="text" id="classRoom" name="classRoom" value="Aktuelles Klassenzimmer" required><br><br>
            <label for="classSchedule">Stundenplan (optional):</label><br>
            <input type="text" id="classSchedule" name="classSchedule" value="Aktueller Stundenplan"><br><br>
            <button type="submit" class="custom-btn" id="configureClassButton">Speichern</button>
        </form>
    `
    document.getElementById('configureClassForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Hier kannst du die Logik zum Bearbeiten der Klasse hinzufügen

        closeDetailView();
    });
}

/*Stundenplan erstellen Formular */

function setDetailInhalt_CreateSchedule() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3>Stundenplan erstellen</h3>
        <hr>
        <form id="createScheduleForm">
            <!-- Formularfelder für den Stundenplan -->
            <label for="scheduleName">Name des Stundenplans:</label><br>
            <input type="text" id="scheduleName" name="scheduleName" required><br><br>
            <label for="scheduleDetails">Details des Stundenplans:</label><br>
            <textarea id="scheduleDetails" name="scheduleDetails" required></textarea><br><br>
            <label for="scheduleEffectiveDate">Gültigkeitsdatum:</label><br>
            <input type="date" id="scheduleEffectiveDate" name="scheduleEffectiveDate" required><br><br>
            <label for="scheduleNotes">Notizen (optional):</label><br>
            <textarea id="scheduleNotes" name="scheduleNotes"></textarea><br><br>
            <button type="submit" class="custom-btn" id="createScheduleButton">Erstellen</button>
        </form>
    `
    document.getElementById('createScheduleForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Hier kannst du die Logik zum Erstellen des Stundenplans hinzufügen

        closeDetailView();
    });
}

function setDetailInhalt_ConfigureSchedule() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3>Stundenplan bearbeiten</h3>
        <hr>
        <form id="configureScheduleForm">
            <!-- Formularfelder für den Stundenplan -->
            <label for="scheduleName">Name des Stundenplans:</label><br>
            <input type="text" id="scheduleName" name="scheduleName" value="Aktueller Stundenplanname" required><br><br>
            <label for="scheduleDetails">Details des Stundenplans:</label><br>
            <textarea id="scheduleDetails" name="scheduleDetails" required>Aktuelle Details des Stundenplans</textarea><br><br>
            <label for="scheduleEffectiveDate">Gültigkeitsdatum:</label><br>
            <input type="date" id="scheduleEffectiveDate" name="scheduleEffectiveDate" value="2024-01-01" required><br><br>
            <label for="scheduleNotes">Notizen (optional):</label><br>
            <textarea id="scheduleNotes" name="scheduleNotes">Aktuelle Notizen</textarea><br><br>
            <button type="submit" class="custom-btn" id="configureScheduleButton">Speichern</button>
        </form>
    `
    document.getElementById('configureScheduleForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Hier kannst du die Logik zum Bearbeiten des Stundenplans hinzufügen

        closeDetailView();
    });
}

/*Event Listener für die Buttons um die Detailansicht zu öffnen*/

button_Schule_erstellen.addEventListener('click', setDetailInhalt_CreateSchool);
button_Schule_bearbeiten.addEventListener('click', setDetailInhalt_ConfigureSchool);
button_Klasse_erstellen.addEventListener('click', setDetailInhalt_CreateClass);
button_Klasse_bearbeiten.addEventListener('click', setDetailInhalt_ConfigureClass);
button_Stundenplan_erstellen.addEventListener('click', setDetailInhalt_CreateSchedule);
button_Stundenplan_bearbeiten.addEventListener('click', setDetailInhalt_ConfigureSchedule);

/*Detailansicht schließen (Hier wird noch eine Logik hinzugefügt um bevor das schließen eine Frage angezeigt bekommen ob er wirklich schließen will)*/
closeButton.addEventListener('click', closeDetailView);