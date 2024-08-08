// Mock the necessary functions and DOM elements
document.body.innerHTML = `
    <div id="updateModal" style="display:none;">
        <form id="updateViewingForm">
            <input type="date" id="preferredDate" />
            <input type="hidden" id="viewingId" />
            <button type="submit"></button>
        </form>
    </div>
    <button class="update-viewing-btn" data-viewing-id="1"></button>
`;

jest.mock('../../static/js/functions/validateDate', () => ({
    validateDate: jest.fn(() => true)
}));
jest.mock('../../static/js/functions/clearModalMessages', () => ({
    clearModalMessages: jest.fn()
}));
jest.mock('../../static/js/functions/getCSRFToken', () => ({
    getCSRFToken: jest.fn(() => 'fake-csrf-token')
}));
jest.mock('../../static/js/functions/showModalMessage', () => ({
    showModalMessage: jest.fn()
}));

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ status: 'ok' })
    })
);

// Mock location.reload to avoid 'not implemented' error
Object.defineProperty(window, 'location', {
    writable: true,
    value: { reload: jest.fn() },
});

require('../../static/js/functions/updateViewing');

describe('Update viewing functionality', () => {
    beforeEach(() => {
        document.getElementById('updateModal').style.display = 'none';
        jest.clearAllMocks();
    });

    test('should show update modal when update button is clicked', () => {
        const updateButton = document.querySelector('.update-viewing-btn');
        updateButton.click();

        const updateModal = document.getElementById('updateModal');
        expect(updateModal.style.display).toBe('block');
    });

    test('should validate and submit the update form', async () => {
        const updateButton = document.querySelector('.update-viewing-btn');
        updateButton.click();

        const updateForm = document.getElementById('updateViewingForm');
        updateForm.dispatchEvent(new Event('submit'));

        expect(require('../../static/js/functions/validateDate').validateDate).toHaveBeenCalledWith('preferredDate');
        expect(require('../../static/js/functions/clearModalMessages').clearModalMessages).toHaveBeenCalled();

        await new Promise(process.nextTick);

        expect(fetch).toHaveBeenCalledWith('/real_estate/update_viewing/1/', expect.any(Object));
        expect(window.location.reload).toHaveBeenCalledTimes(1);
    });
});
