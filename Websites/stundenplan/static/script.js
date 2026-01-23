/* 
Willkommen in der Javascript Datei.

JavaScript (Frontend): Wird verwendet für Aktionen, die direkt im Browser des Benutzers ausgeführt 
werden – wie DOM-Manipulation (Elemente anzeigen/ausblenden), 
Validierung von Formularen oder das Anzeigen von Popups.
*/

//Dieses Event wird ausgeführt wenn das "Document" (Website) geladen wurde.
document.addEventListener('DOMContentLoaded', function() {
    console.log("Die Website wurde geladen.")
});

const underlay = document.getElementById('underlay_popup');
const popup = document.getElementById('abmelde_popup');


const abmelde_button = document.getElementById('abmelden');
const abmelde_button_dropdown = document.getElementById('abmelden_dropmenu');
const abbruch_button = document.getElementById('abbruch_button');
const abmelde_button_div = document.getElementById('abmelde_button');

function zeigeAbmeldePopup(){
    popup.style.display = 'block';
    underlay.style.display = 'block';

    setTimeout(() => {
        popup.style.opacity = '1';
        underlay.style.opacity = '1';
    });
}

function versteckeAbmeldePopup(){
    setTimeout(()=> {
        underlay.style.opacity = '0';
        popup.style.opacity = '0';
    });

    popup.style.display = 'none';
    underlay.style.display = 'none';
}

function abmelden(){
    window.location.href = "/logout/";
}

abmelde_button.addEventListener('click', zeigeAbmeldePopup);
abmelde_button_dropdown.addEventListener('click', zeigeAbmeldePopup);
abbruch_button.addEventListener('click', versteckeAbmeldePopup);
abmelde_button_div.addEventListener('click', abmelden);

underlay.addEventListener('click', versteckeAbmeldePopup);

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        versteckeAbmeldePopup();
    }
});

//Kalender
const calendarEl = document.getElementById("calendar");
const monthYearEl = document.getElementById("monthYear");

let currentDate = new Date();

const days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
const months = [
  "Januar", "Februar", "März", "April", "Mai", "Juni",
  "Juli", "August", "September", "Oktober", "November", "Dezember"
];

function renderCalendar() {
  calendarEl.innerHTML = "";
  monthYearEl.textContent =
    `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;

  // Wochentage
  days.forEach(day => {
    const div = document.createElement("div");
    div.textContent = day;
    div.className = "day-name";
    calendarEl.appendChild(div);
  });

  const firstDay = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    1
  ).getDay() || 7;

  const daysInMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    0
  ).getDate();

  // Leere Felder
  for (let i = 1; i < firstDay; i++) {
    calendarEl.appendChild(document.createElement("div"));
  }

  // Tage
  for (let day = 1; day <= daysInMonth; day++) {
    const div = document.createElement("div");
    div.textContent = day;
    div.className = "day";

    const today = new Date();
    if (
      day === today.getDate() &&
      currentDate.getMonth() === today.getMonth() &&
      currentDate.getFullYear() === today.getFullYear()
    ) {
      div.classList.add("today");
    }

    calendarEl.appendChild(div);
  }
}

function changeMonth(step) {
  currentDate.setMonth(currentDate.getMonth() + step);
  renderCalendar();
}

renderCalendar();

//Notizen
const notes = JSON.parse(localStorage.getItem("notes")) || {};

const dateInput = document.getElementById("noteDate");
const noteText = document.getElementById("noteText");

dateInput.valueAsDate = new Date();

dateInput.onchange = loadNote;

function loadNote() {
  const key = dateInput.value;
  noteText.value = notes[key] || "";
}

function saveNote() {
  const key = dateInput.value;
  const text = noteText.value.trim();

  if (!key) return;

  if (text) {
    notes[key] = text;
  } else {
    delete notes[key];
  }

  localStorage.setItem("notes", JSON.stringify(notes));
  alert("Gespeichert!");
}

function deleteNote() {
  const key = dateInput.value;
  delete notes[key];
  localStorage.setItem("notes", JSON.stringify(notes));
  noteText.value = "";
}
