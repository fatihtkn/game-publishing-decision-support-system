const sideMenu = document.getElementById('sideMenu');

sideMenu.addEventListener('mouseenter', () => {
    sideMenu.classList.add('expanded');
});

sideMenu.addEventListener('mouseleave', () => {
    sideMenu.classList.remove('expanded');
});
