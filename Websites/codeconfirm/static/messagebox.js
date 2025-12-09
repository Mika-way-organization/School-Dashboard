document.getElementById("verification-form").addEventListener("submit", function(e){
    e.preventDefault();

    const form = e.target;
    const messageContainer = document.getElementById("message-container");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const formData = {
        code: form.code.value
    }

    messageContainer.style.display = "flex";
    messageContainer.textContent = '';
    messageContainer.classList.remove('success-box');
    messageContainer.classList.add('error-box');

    messageContainer.style.display = "flex";
    messageContainer.textContent = '';
    messageContainer.classList.remove('success-box');
    messageContainer.classList.add('error-box');

    fetch('/codeconfirm_data/require', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(formData)
    })
    .then(async response => {
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
    })
    .then(result => {
        const { status, body } = result;
        if (status === 200 && body.status === "success") {
            messageContainer.classList.remove('error-box');
            messageContainer.classList.add('success-box');
            messageContainer.textContent = body.message;
            setTimeout(() => {
                window.location.href = '/login';
            }, 1500);
        } else {
            messageContainer.textContent = body.message || 'Ein unbekannter Fehler ist aufgetreten.';
            messageContainer.style.display = "flex";
        }
    })
    .catch(error => {
        messageContainer.textContent = 'Netzwerkfehler. Bitte versuchen Sie es erneut. ' + error;
        console.error('Error:', error);
    });
});