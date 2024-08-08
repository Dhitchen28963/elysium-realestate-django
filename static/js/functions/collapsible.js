function setupCollapsible() {
    const collapsibles = document.querySelectorAll('.collapsible');
    collapsibles.forEach(collapsible => {
        collapsible.addEventListener('click', function () {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        });
    });
}

function setupCloseCollapsible() {
    const closeButtons = document.querySelectorAll('.close-collapsible');
    closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const content = this.parentElement;
            content.style.display = 'none';
            const collapsible = content.previousElementSibling;
            if (collapsible.classList.contains('collapsible')) {
                collapsible.classList.remove('active');
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });
}

module.exports = {
    setupCollapsible,
    setupCloseCollapsible
};
