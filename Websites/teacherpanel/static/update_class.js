
export function update_class_submit() {
    document.getElementById('configureClassForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const form = e.target;
        const messageContainer = document.getElementById("configureClassTitle");
        const detailView = document.getElementById("detailView");
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const formData = {
            className: form.className.value,
            classGrade: form.classGrade.value,
            classGroupe: form.classGroupe.value,
            classRoom: form.classRoom.value,
            classTeacher: form.classTeacher.value,
            classStudent: form.classStudent.value
        }

        fetch('/save_class_data/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(formData)
        }).then(async response => {
            const text = await response.text();
            let data;
            console.log(text);
            
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
                messageContainer.textContent = 'Klasse erfolgreich bearbeitet!';
                setTimeout(() => {
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                    messageContainer.textContent = "Klasse bearbeiten";
                    window.location.reload();
                }, 1500);
                
            } else {
                messageContainer.innerHTML = 'Klasse nicht bearbeitet!<br> <p style="font-size: 14px; color: red;">' + body.message + '</p>';
                detailView.style.border = '6px solid rgba(255, 0, 0, 0.64)';

                setTimeout(() => {
                    messageContainer.textContent = "Klasse bearbeiten";
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                }, 10000);
            }
        })
    });
}