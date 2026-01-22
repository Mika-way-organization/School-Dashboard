/*
In ideser Datei wird das Automatische holen von Daten des /dashabord_data geschrieben.
*/

/* Berechnet die Millisekunden bis zur nächsten vollen Minute */
function getMillisecondsUntilNextMinute() {
    const now = new Date();
    return (60 - now.getSeconds()) * 1000 - now.getMilliseconds();
}
/* Lädt die Dashboard-Daten vom Server und aktualisiert die HTML-Elemente */
function loadDashboardData(){
    fetch('/dashboard_data').then(response => {
        if (!response.ok) {
            throw new Error('Netzwerkantwort war nicht ok', response.statusText);
        }
        return response.json();
    }).then(data => {
        const time_date = document.getElementById('time-date');
        const wetter_icon = document.getElementById('wetter_icon');
        const description_w = document.getElementById('description_w');
        const temp = document.getElementById('temp');
        const humidity = document.getElementById('humidity');
        const city = document.getElementById('city');
        const joke_text = document.getElementById('joke_text');
        const subject = document.getElementById('div2_fach');
        const teacher = document.getElementById('div2_teacher');
        const room = document.getElementById('div2_room');
        const homework = document.getElementById('div3_homework');
        const schoolwork = document.getElementById('div3_schoolwork');
        const sonstiges = document.getElementById('div3_sonstiges');

        const one_subject = document.getElementById('one_subject');
        const two_subject = document.getElementById('two_subject');
        const three_subject = document.getElementById('three_subject');
        const four_subject = document.getElementById('four_subject');
        const five_subject = document.getElementById('five_subject');
        const six_subject = document.getElementById('six_subject');
        const seven_subject = document.getElementById('seven_subject');
        const eight_subject = document.getElementById('eight_subject');

        const one_room = document.getElementById('one_room');
        const two_room = document.getElementById('two_room');
        const three_room = document.getElementById('three_room');
        const four_room = document.getElementById('four_room');
        const five_room = document.getElementById('five_room');
        const six_room = document.getElementById('six_room');
        const seven_room = document.getElementById('seven_room');
        const eight_room = document.getElementById('eight_room');

        time_date.innerHTML = ` ${data.time} <br> ${data.date} `;
        wetter_icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        wetter_icon.alt = `Icon: ${data.weather_description}`;
        wetter_icon.title = `Aktuell: ${data.weather_description}`;
        description_w.innerHTML = ` ${data.weather_description} `;
        temp.innerHTML = ` Temperatur: ${data.temperatur}°C Gefühlt: ${data.feels_like}°C `;
        humidity.innerHTML = ` Luftfeuchtigkeit: ${data.humidity}% `;
        city.innerHTML = ` Stadt: ${data.city} `;
        joke_text.innerHTML = ` ${data.joke} `;

        subject.innerHTML = ` Fach: ${data.subject} `;
        teacher.innerHTML = ` Lehrer: ${data.teacher_id} `;
        room.innerHTML = ` Raum: ${data.room} `;

        homework.innerHTML = `${data.homework}`;
        sonstiges.innerHTML = `${data.note}`;

        one_subject.innerHTML = `${data.first_lesson.subject}`;
        two_subject.innerHTML = `${data.second_lesson.subject}`;
        three_subject.innerHTML = `${data.third_lesson.subject}`;
        four_subject.innerHTML = `${data.fourth_lesson.subject}`;
        five_subject.innerHTML = `${data.fifth_lesson.subject}`;
        six_subject.innerHTML = `${data.sixth_lesson.subject}`;
        seven_subject.innerHTML = `${data.seventh_lesson.subject}`;
        eight_subject.innerHTML = `${data.eighth_lesson.subject}`;

        one_room.innerHTML = `${data.first_lesson.room}`;
        two_room.innerHTML = `${data.second_lesson.room}`;
        three_room.innerHTML = `${data.third_lesson.room}`;
        four_room.innerHTML = `${data.fourth_lesson.room}`;
        five_room.innerHTML = `${data.fifth_lesson.room}`;
        six_room.innerHTML = `${data.sixth_lesson.room}`;
        seven_room.innerHTML = `${data.seventh_lesson.room}`;
        eight_room.innerHTML = `${data.eighth_lesson.room}`;

        console.log("Dashboard Daten wurden aktualisiert." + data.first_lesson);
    }).catch(error => {
        console.error('Fehler beim Laden der Dashboard-Daten:', error);
    }).finally(() => {
        scheduleNextUpdate();
    })
}
/* Lädt die Dashboard-Daten und plant das nächste Update */
function scheduleNextUpdate() {
    const delay = getMillisecondsUntilNextMinute();
    setTimeout(loadDashboardData, delay);
}

scheduleNextUpdate();