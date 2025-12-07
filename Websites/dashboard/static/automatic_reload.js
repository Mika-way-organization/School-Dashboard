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

        time_date.innerHTML = ` ${data.time} <br> ${data.date} `;
        wetter_icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        wetter_icon.alt = `Icon: ${data.weather_description}`;
        wetter_icon.title = `Aktuell: ${data.weather_description}`;
        description_w.innerHTML = ` ${data.weather_description} `;
        temp.innerHTML = ` Temperatur: ${data.temperatur}°C Gefühlt: ${data.feels_like}°C `;
        humidity.innerHTML = ` Luftfeuchtigkeit: ${data.humidity}% `;
        city.innerHTML = ` Stadt: ${data.city} `;
        joke_text.innerHTML = ` ${data.joke} `;
        console.log("Dashboard Daten wurden aktualisiert.");
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