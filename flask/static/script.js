const btn = document.querySelector('#trending-btn');
const dataEl = document.querySelector('#trending-data');

btn.addEventListener('click', () => {
  fetch('/data')
    .then(response => response.text())
    .then(data => dataEl.textContent = data)
    .catch(error => console.error(error));
});
