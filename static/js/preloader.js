// Preloader JavaScript -> Es fügt jeder Website eine Ladeanimation hinzu
const preloaderHTML = `<div id="preloader-wrapper"><div class='pac-man' id='pacman_preloader'></div></div>`;

document.addEventListener("DOMContentLoaded", function () {
  document.body.insertAdjacentHTML("afterbegin", preloaderHTML);
});

window.addEventListener("load", function () {
  const preloader = document.getElementById("preloader-wrapper");
  if (preloader) {
    setTimeout(function () {
      preloader.classList.add("hidden");
      setTimeout(function () {
        preloader.remove();
      }, 50);
    }, 10);
  }
});
