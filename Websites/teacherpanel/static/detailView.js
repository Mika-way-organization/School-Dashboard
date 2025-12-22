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
        <h3>Schule erstellen</h3>
        <hr>
        <form id="createSchoolForm">
            <label for="schoolName">Name der Schule:</label><br>
            <input type="text" id="schoolName" name="schoolName" required><br><br>
            <label for="schoolAddress">Adresse der Schule:</label><br>
            <input type="text" id="schoolAddress" name="schoolAddress" required><br><br>
            <button type="submit" class="custom-btn" id="createSchoolButton">Erstellen</button>
        </form>
    `
    document.getElementById('createSchoolForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Hier kannst du die Logik zum Erstellen der Schule hinzufügen

        closeDetailView();
    });
}

function setDetailInhalt_ConfigureSchool() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3>Schule bearbeiten</h3>
        <hr>
        <form id="configureSchoolForm">
            <label for="schoolName">Name der Schule:</label><br>
            <input type="text" id="schoolName" name="schoolName" value="Aktueller Schulname" required><br><br>
            <label for="schoolAddress">Adresse der Schule:</label><br>
            <input type="text" id="schoolAddress" name="schoolAddress" value="Aktuelle Schuladresse" required><br><br>
            <button type="submit" class="custom-btn" id="configureSchoolButton">Speichern</button>
        </form>
    `
    document.getElementById('configureSchoolForm').addEventListener('submit', function(event) {
        event.preventDefault();

        // Hier kannst du die Logik zum Bearbeiten der Schule hinzufügen

        closeDetailView();
    });
}

/*Klasse erstellen Formular */

function setDetailInhalt_CreateClass() {
    openDetailView();
    detailInhalt.innerHTML = `
        <h3>Klasse erstellen</h3>
        <hr>
        <form id="createClassForm">
            <label for="className">Name der Klasse:</label><br>
            <input type="text" id="className" name="className" required><br><br>
            <label for="classGrade">Klassenstufe:</label><br>
            <input type="number" id="classGrade" name="classGrade" required><br><br>
            <label for="classTeacher">Klassenlehrer:</label><br>
            <input type="text" id="classTeacher" name="classTeacher" required><br><br>
            <label for="classRoom">Klassenzimmer:</label><br>
            <input type="text" id="classRoom" name="classRoom" required><br><br>
            <label for="classSchedule">Stundenplan (optional):</label><br>
            <input type="text" id="classSchedule" name="classSchedule"><br><br>
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