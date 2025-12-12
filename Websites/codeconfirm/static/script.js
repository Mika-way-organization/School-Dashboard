/* 
Willkommen in der Javascript Datei.

JavaScript (Frontend): Wird verwendet für Aktionen, die direkt im Browser des Benutzers ausgeführt 
werden – wie DOM-Manipulation (Elemente anzeigen/ausblenden), 
Validierung von Formularen oder das Anzeigen von Popups.
*/

// DIESE DTAEI IST NOCH IN ARBEIT!

//Dieses Event wird ausgeführt wenn das "Document" (Website) geladen wurde.
document.addEventListener('DOMContentLoaded', function () {
    console.log("Die Website wurde nicht gefunden.")
});

document.getElementById("new_code").addEventListener("click", function () {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const Message = {
        status: "request_new_code",
    }


    const messageContainer = document.getElementById("message-container");

    messageContainer.style.display = "flex";
    messageContainer.textContent = '';
    messageContainer.classList.remove('success-box');
    messageContainer.classList.add('error-box');

    fetch('/codeconfirm/new_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(Message)
    }).then(async response => {

        const text = await response.text();
        // Versuche, den Text in JSON zu parsen
        let data;
        try {
            data = JSON.parse(text);
        } catch (err) {
            console.error("Fehler beim Parsen von JSON:", err);
            throw err;
        }
        return { status: response.status, body: data };
    }).catch(error => {
        messageContainer.textContent = 'Netzwerkfehler. Bitte versuchen Sie es erneut. ' + error;
        console.error('Error:', error);
    });
});