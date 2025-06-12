document.getElementById('botonEnviar').addEventListener('click', () => {
  alert('Aquí podrías agregar la función para enviar un sitio.');
});

const slides = document.querySelectorAll('.slide');
const prevBtn = document.querySelector('.carrusel .prev');
const nextBtn = document.querySelector('.carrusel .next');
let current = 0;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.classList.toggle('visible', i === index);
  });
  current = index;
}

prevBtn.addEventListener('click', () => {
  let nextIndex = current - 1;
  if (nextIndex < 0) nextIndex = slides.length - 1;
  showSlide(nextIndex);
});

nextBtn.addEventListener('click', () => {
  let nextIndex = current + 1;
  if (nextIndex >= slides.length) nextIndex = 0;
  showSlide(nextIndex);
});

// Auto slide cada 5 segundos
setInterval(() => {
  let nextIndex = current + 1;
  if (nextIndex >= slides.length) nextIndex = 0;
  showSlide(nextIndex);
}, 5000);
