
export function create_timetable_submit() {
    document.getElementById('createScheduleForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const form = e.target;
        const messageContainer = document.getElementById("createScheduleTitle");
        const detailView = document.getElementById("detailView");
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        const formData = {
            scheduleSubject: form.scheduleSubject.value,
            scheduleTeacher: form.scheduleTeacher.value,
            scheduleDay: form.scheduleDay.value,
            scheduleStartTime: form.scheduleStartTime.value,
            scheduleEndTime: form.scheduleEndTime.value,
            scheduleRoom: form.scheduleRoom.value,
            scheduleHomework: form.scheduleHomework.value,
            scheduleNotes: form.scheduleNotes.value
        }

        fetch('/save_timetable_data/require', {
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
            if (status === 201 && body.status === "success") {
                detailView.style.border = '6px solid rgba(81, 255, 0, 0.64)';
                messageContainer.textContent = 'Stundenplan erfolgreich erstellt!';
                setTimeout(() => {
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                    messageContainer.textContent = "Stundenplan erstellen";
                    window.location.reload();
                }, 1500);
                
            } else {
                messageContainer.innerHTML = 'Stundenplan nicht erstellt!<br> <p style="font-size: 14px; color: red;">' + body.message + '</p>';
                detailView.style.border = '6px solid rgba(255, 0, 0, 0.64)';

                setTimeout(() => {
                    messageContainer.textContent = "Stundenplan erstellen";
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                }, 10000);
            }
        }).catch(error => {
            console.error('Fehler bei der Anfrage:', error);
            messageContainer.innerHTML = 'Ein Fehler ist aufgetreten!<br> <p style="font-size: 14px; color: red;">Bitte versuchen Sie es erneut.</p>';
            detailView.style.border = '6px solid rgba(255, 0, 0, 0.64)';

            setTimeout(() => {
                messageContainer.textContent = "Stundenplan erstellen";
                detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
            }, 10000);
        });
    });
}