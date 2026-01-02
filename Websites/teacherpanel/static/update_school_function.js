/* Hier wird die funktion zum Aktualisieren der Schul Daten implementiert */

export function update_school_submit() {
    document.getElementById('configureSchoolForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const form = e.target;
        const messageContainer = document.getElementById("configureSchoolTitle");
        const detailView = document.getElementById("detailView");
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const formData = {
            schoolName: form.schoolName.value,
            email: form.schoolEmail.value,
            phone: form.schoolPhone.value,
            postalcode: form.schoolpostalcode.value,
            city: form.schoolcity.value,
            street: form.schoolstreet.value,
            housenumber: form.schoolhouseNumber.value,
            state: form.schoolstate.value,
            country: form.schoolcountry.value
        }

        fetch('/save_school_data/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        }) .then(async response => {
            const text = await response.text();
            let data;
            try {
                data = JSON.parse(text);
            } catch (err) {
                console.error("Fehler beim Parsen von JSON:", err);
                throw err;
            }
            return { status: response.status, body: data };
        }).then(result => {
            const { status, body } = result;
            if (status === 200 && body.status === "success") {
                detailView.style.border = '6px solid rgba(81, 255, 0, 0.64)';
                messageContainer.textContent = 'Schule erfolgreich bearbeitet!';
                setTimeout(() => {
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                    messageContainer.textContent = "Schule bearbeiten";
                    window.location.reload();
                }, 1500);

            } else {
                messageContainer.innerHTML = 'Schule nicht bearbeitet!<br> <p style="font-size: 14px; color: red;">' + body.message + '</p>';
                detailView.style.border = '6px solid rgba(255, 0, 0, 0.64)';

                setTimeout(() => {
                    messageContainer.textContent = "Schule bearbeiten";
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                }, 10000)
            }
        })
    });
}