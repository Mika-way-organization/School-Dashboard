/*
Hier wird die funktion für die 'create_class' erstellt.

*/

export function create_class_submit() {
    document.getElementById('createClassForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const form = e.target;
        const messageContainer = document.getElementById("createClassTitle");
        const detailView = document.getElementById("detailView");
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        
    })
}