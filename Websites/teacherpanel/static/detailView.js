// Detail Ansicht Elemente
const detailView = document.getElementById('detailView');
const detailInhalt = document.getElementById('detail_inhalt');
const underlayDetail = document.getElementById('underlay_detail');
const closeButton = document.getElementById('closeButton');

const button_Schule_erstellen = document.getElementById('Schule_erstellen');
const button_Schule_bearbeiten = document.getElementById('Schule_bearbeiten');
const button_Klasse_erstellen = document.getElementById('Klasse_erstellen');
const button_Klasse_bearbeiten = document.getElementById('Klasse_bearbeiten');
const button_Stundenplan_erstellen = document.getElementById('Stundenplan_erstellen');
const button_Stundenplan_bearbeiten = document.getElementById('Stundenplan_bearbeiten');

function closeDetailView() {
    detailView.style.display = 'none';
    underlayDetail.style.display = 'none';

    setTimeout(() => {
        underlayDetail.style.opacity = '0';
        detailView.style.opacity = '0';
    });
}

function openDetailView() {
    detailView.style.display = 'block';
    underlayDetail.style.display = 'block';
    
    setTimeout(() => {
        detailView.style.opacity = '1';
        underlayDetail.style.opacity = '1';
    });
}

button_Schule_erstellen.addEventListener('click', openDetailView);
button_Schule_bearbeiten.addEventListener('click', openDetailView);
button_Klasse_erstellen.addEventListener('click', openDetailView);
button_Klasse_bearbeiten.addEventListener('click', openDetailView);
button_Stundenplan_erstellen.addEventListener('click', openDetailView);
button_Stundenplan_bearbeiten.addEventListener('click', openDetailView);

closeButton.addEventListener('click', closeDetailView);
underlayDetail.addEventListener('click', closeDetailView);

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeDetailView();
    }
});