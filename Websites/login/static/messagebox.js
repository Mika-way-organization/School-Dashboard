document.getElementById("login_form").addEventListener("submit", function(e){
    e.preventDefault();  // Verhindert das automatische Absenden des Formulars

    const form = e.target;
    const formData = new FormData(form);
})