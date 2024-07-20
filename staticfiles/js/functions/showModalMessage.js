function showModalMessage(message) {
    const modalMessage = document.getElementById('modalMessage');
    const modal = document.getElementById('messageModal');
    if (modalMessage && modal) {
        modalMessage.textContent = message;
        modal.style.display = 'block';

        const closeModal = document.querySelector('.close');
        if (closeModal) {
            closeModal.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }
    }
}

module.exports = showModalMessage;