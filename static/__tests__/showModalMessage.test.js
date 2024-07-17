// static/__tests__/showModalMessage.test.js
const showModalMessage = require('../js/functions/showModalMessage');

describe('showModalMessage', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="messageModal" style="display: none;">
                <div id="modalMessage"></div>
                <button class="close">Close</button>
            </div>
        `;
    });

    test('should show modal message with correct content', () => {
        const message = 'Test message';
        showModalMessage(message);
        const modalMessage = document.getElementById('modalMessage');
        expect(modalMessage.textContent).toBe(message);
        const modal = document.getElementById('messageModal');
        expect(modal.style.display).toBe('block');
    });

    test('should hide modal when close button is clicked', () => {
        showModalMessage('Test message');
        const closeModal = document.querySelector('.close');
        closeModal.click();
        const modal = document.getElementById('messageModal');
        expect(modal.style.display).toBe('none');
    });
});