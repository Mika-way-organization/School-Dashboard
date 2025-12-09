/*Willkommen in der Javascript Datei.*/

// Holt für die Alert-Funktion die benötigten Elemente
const alertFunction = document.getElementById('alert_function');
const alertH2 = document.getElementById('alert_h2');
const alertP = document.getElementById('alert_p');
const alertButton = document.getElementById('alert_button');
// Diese Element wird von dem preloader Code verwendet
const underlay = document.getElementById('underlay_popup');


function showAlert(title, message) {
    alertFunction.style.display = 'block';
    underlay.style.display = 'block';

    setTimeout(() => {
        alertFunction.style.opacity = '1';
        underlay.style.opacity = '1';
    })
}

function hideAlert() {
    setTimeout(() => {
        alertFunction.style.opacity = '0';
        underlay.style.opacity = '0';
    })
    alertFunction.style.display = 'none';
    underlay.style.display = 'none';
}

// Event-Listener für den Alert-Button
alertButton.addEventListener('click', hideAlert);