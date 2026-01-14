
export function create_timetable_submit() {
    document.getElementById('ScheduleForm').addEventListener('submit', function(e) {
        e.preventDefault();

        const buttonValue = document.getElementById('ScheduleButton').textContent;
        console.log("Button Value:", buttonValue);

        if (buttonValue === "Erstellen") {

            const form = e.target;
            const messageContainer = document.getElementById("scheduleTitle");
            const detailView = document.getElementById("detailView");
            const dateInput = document.getElementById('selectedDate');
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            const formData = {
                scheduleSubject: form.scheduleSubject.value,
                scheduleTeacher: form.scheduleTeacher.value,
                scheduleDay: dateInput.value,
                lessonHour: form.lessonHour.value,
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
        }else if (buttonValue === "Speichern") {
            // Ähnliche Logik für das Speichern des Stundenplans
            // ...
        }
    });
}

export function date_event_listener() {
    const dateInput = document.getElementById('selectedDate');
    dateInput.addEventListener('change', function() {
        const selectedDate = new Date(this.value);
        const messageContainer = document.getElementById("scheduleTitle");
        const detailView = document.getElementById("detailView");
        const scheduleButton = document.getElementById("ScheduleButton");
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        fetch('/give_timetable_data/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ date: selectedDate.toISOString().split('T')[0]})
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

                messageContainer.textContent = "Stundenplan bearbeiten";
                scheduleButton.textContent = "Speichern";

                document.getElementById('scheduleSubject').value = body.data.scheduleSubject;
                document.getElementById('scheduleTeacher').value = body.data.scheduleTeacher;
                document.getElementById('lessonHour').value = body.data.schedulelessenHour;
                document.getElementById('scheduleRoom').value = body.data.scheduleRoom;
                document.getElementById('scheduleHomework').value = body.data.scheduleHomework;
                document.getElementById('scheduleNotes').value = body.data.scheduleNotes;
            } else if (status === 404 && body.status === "miss") {

                messageContainer.textContent = "Neuen Stundenplan erstellen";
                scheduleButton.textContent = "Erstellen";

                document.getElementById('scheduleSubject').value = '';
                document.getElementById('scheduleTeacher').value = '';
                document.getElementById('lessonHour').value = '';
                document.getElementById('scheduleRoom').value = '';
                document.getElementById('scheduleHomework').value = '';
                document.getElementById('scheduleNotes').value = '';
            } else {
                messageContainer.innerHTML = 'Stundenplan Fehler<br> <p style="font-size: 14px; color: red;">' + body.message + '</p>';
                detailView.style.border = '6px solid rgba(255, 0, 0, 0.64)';

                setTimeout(() => {
                    messageContainer.textContent = "Stundenplan";
                    detailView.style.border = '4px solid rgba(71, 226, 0, 0.5)';
                }, 10000);
            }
        })
    });
}