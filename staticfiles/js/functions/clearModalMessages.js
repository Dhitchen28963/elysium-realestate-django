function clearModalMessages() {
    const modal = document.getElementById('messageModal');
    const modalMessage = document.getElementById('modalMessage');
    
    if (modalMessage) {
        modalMessage.textContent = '';
    }
    
    if (modal) {
        modal.style.display = 'none';
    }
}

module.exports = clearModalMessages;