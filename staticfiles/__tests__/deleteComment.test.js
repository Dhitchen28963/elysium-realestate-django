// Mock the necessary functions
jest.mock('../../static/js/functions/getCSRFToken', () => ({
    getCSRFToken: jest.fn(() => 'fake-csrf-token')
}));
jest.mock('../../static/js/functions/showModalMessage', () => ({
    showModalMessage: jest.fn((message) => console.log('Modal Message:', message))
}));

const { getCSRFToken } = require('../../static/js/functions/getCSRFToken');
const { showModalMessage } = require('../../static/js/functions/showModalMessage');

// Mock the necessary DOM elements
document.body.innerHTML = `
    <div id="modalMessage" style="display: none;"></div>
    <div id="deleteModal" style="display: none;"></div>
    <button class="delete-comment" data-id="1">Delete</button>
    <button id="confirmDelete">Confirm Delete</button>
    <div id="comment-1"></div>
`;

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ success: true }),
    })
);

require('../../static/js/functions/deleteComment');

describe('Delete comment functionality', () => {
    beforeEach(() => {
        document.getElementById('deleteModal').style.display = 'none';
        jest.clearAllMocks();
    });

    test('should show delete modal when delete button is clicked', () => {
        const deleteButton = document.querySelector('button.delete-comment');
        deleteButton.click();

        const deleteModal = document.getElementById('deleteModal');
        expect(deleteModal.style.display).toBe('block');
    });

    test('should call fetch and delete the comment', async () => {
        const deleteButton = document.querySelector('button.delete-comment');
        deleteButton.click();

        const confirmDeleteButton = document.getElementById('confirmDelete');
        confirmDeleteButton.click();

        await new Promise(process.nextTick); // Ensure fetch completes

        expect(fetch).toHaveBeenCalledWith('/blog/comment/1/delete/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': 'fake-csrf-token',
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        expect(fetch).toHaveBeenCalledTimes(1);
    });
});
