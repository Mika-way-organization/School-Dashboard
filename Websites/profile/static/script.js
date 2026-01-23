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
abbruch_button.addEventListener('click', versteckeAbmeldePopup);
abmelde_button_div.addEventListener('click', abmelden);
