// Import the function to be tested
const clearModalMessages = require('../../static/js/functions/clearModalMessages');

// Set up the DOM for testing
beforeEach(() => {
    document.body.innerHTML = `
        <div id="messageModal" style="display:block;">
            <div id="modalMessage">Test Message</div>
        </div>
    `;
});

// Test cases
describe('clearModalMessages', () => {
    test('should clear the modal message content', () => {
        clearModalMessages();
        const modalMessage = document.getElementById('modalMessage');
        expect(modalMessage.textContent).toBe('');
    });

    test('should hide the modal', () => {
        clearModalMessages();
        const modal = document.getElementById('messageModal');
        expect(modal.style.display).toBe('none');
    });

    test('should not throw an error if modalMessage is not found', () => {
        document.body.innerHTML = ''; // Clear the DOM to ensure the modalMessage element does not exist
        expect(() => clearModalMessages()).not.toThrow();
    });
});