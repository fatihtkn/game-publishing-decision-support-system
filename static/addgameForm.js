// Buton ve modal elemanlarını seçin
const addGameButton = document.getElementById('addGameButton');
const modal = document.getElementById('modal');
const closeModal = document.getElementById('closeModal');

// "Oyun Ekle" butonuna tıklayınca modal açılır
addGameButton.addEventListener('click', () => {
    modal.classList.add('show');
});

// Modal kapatma butonuna tıklayınca modal kapanır
closeModal.addEventListener('click', () => {
    modal.classList.remove('show');
});

// Modal dışında bir yere tıklanırsa modal kapanır
window.addEventListener('click', (event) => {
    if (event.target == modal) {
        modal.classList.remove('show');
    }
});
