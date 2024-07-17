const requestCustomViewing = require('../../static/js/functions/requestCustomViewing');

// Mock fetch API for testing purposes
global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ status: 'ok' }),
        ok: true,
    })
);

// Mock FormData for testing purposes
global.FormData = function () {
    this.append = jest.fn();
};

// Mock validateDate function
jest.mock('../../static/js/functions/validateDate', () => ({
    validateDate: jest.fn(() => true),
}));

// Mock getCSRFToken function
jest.mock('../../static/js/functions/getCSRFToken', () => jest.fn(() => 'mock-csrf-token'));

// Mock showModalMessage function
jest.mock('../../static/js/functions/showModalMessage', () => jest.fn());

describe('requestCustomViewing', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <form id="custom-viewing-form">
                <input type="date" id="preferred_date" />
            </form>
            <div id="viewingModal"></div>
        `;
        global.fetch.mockClear();
    });

    test('should send custom viewing request successfully', async () => {
        const propertyId = 1;
        await expect(requestCustomViewing(propertyId)).resolves.toEqual(expect.objectContaining({
            status: 'ok'
        }));
        expect(global.fetch).toHaveBeenCalled();
    });

    test('should handle error sending custom viewing request', async () => {
        const propertyId = 2;
        global.fetch.mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({ status: 'error' }),
                ok: false,
            })
        );

        await expect(requestCustomViewing(propertyId)).rejects.toThrow('Network response was not ok');
    });

    test('should handle invalid date when sending custom viewing request', async () => {
        const { validateDate } = require('../../static/js/functions/validateDate');
        validateDate.mockReturnValueOnce(false); // Mock invalid date scenario
        const propertyId = 3;
        await expect(requestCustomViewing(propertyId)).resolves.toBe(undefined); // Expect undefined as validateDate failed
        expect(global.fetch).not.toHaveBeenCalled();
    });
});