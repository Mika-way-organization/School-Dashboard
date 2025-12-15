// Detail Ansicht Elemente
const detailView = document.getElementById('detailView');
const detailInhalt = document.getElementById('detail_inhalt');
const underlayDetail = document.getElementById('underlay_detail');
const closeButton = document.getElementById('closeButton');

const subject = document.getElementById('div2');
const homework = document.getElementById('div3');
const JokesNews = document.getElementById('div4');
const time = document.getElementById('div5');
const weather = document.getElementById('div6');
const tableview = document.getElementById('div7');

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

subject.addEventListener('click', openDetailView);
homework.addEventListener('click', openDetailView);
JokesNews.addEventListener('click', openDetailView);
time.addEventListener('click', openDetailView);
weather.addEventListener('click', openDetailView);
tableview.addEventListener('click', openDetailView);

closeButton.addEventListener('click', closeDetailView);
underlayDetail.addEventListener('click', closeDetailView);

document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        closeDetailView();
    }
});