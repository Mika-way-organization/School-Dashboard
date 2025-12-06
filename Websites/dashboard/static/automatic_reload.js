/*
In ideser Datei wird das Automatische holen von Daten des /dashabord_data geschrieben.
*/
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

        time_date.innerHTML = ` ${data.time} <br> ${data.date} `;
        wetter_icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        wetter_icon.alt = `Icon: ${data.weather_description}`;
        wetter_icon.title = `Aktuell: ${data.weather_description}`;
        description_w.innerHTML = ` ${data.weather_description} `;
        temp.innerHTML = ` Temperatur: ${data.temperatur}°C Gefühlt: ${data.feels_like}°C `;
        humidity.innerHTML = ` Luftfeuchtigkeit: ${data.humidity}% `;
        city.innerHTML = ` Stadt: ${data.city} `;
        console.log("Dashboard Daten wurden aktualisiert.");
    }).catch(error => {
        console.error('Fehler beim Laden der Dashboard-Daten:', error);
    })
}

setInterval(loadDashboardData, 60000); // Alle 1 Minuten aktualisieren