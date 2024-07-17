// addToFavorites.test.js

const addToFavorites = require('../../static/js/functions/addToFavorites');

// Mock fetch API for testing purposes
global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ status: 'ok' }),
        ok: true,
    })
);

// Set up the DOM for testing (optional for this test case)
beforeEach(() => {
    // You can set up the DOM structure if needed
});

console.log('Testing addToFavorites');

// Test cases
describe('addToFavorites', () => {
    test('should add property to favorites successfully', async () => {
        const propertyId = 1;
        const app = 'real_estate';
        const mockShowModalMessage = jest.fn(); // Mock showModalMessage function

        // Call addToFavorites with mocked showModalMessage
        await expect(addToFavorites(propertyId, app, mockShowModalMessage)).resolves.toEqual(expect.objectContaining({
            status: 'ok'
        }));

        // Verify showModalMessage was called with the success message
        expect(mockShowModalMessage).toHaveBeenCalledWith('Property added to favorites!');
    });

    test('should handle error adding property to favorites', async () => {
        const propertyId = 2;
        const app = 'real_estate';
        const mockShowModalMessage = jest.fn(); // Mock showModalMessage function
        global.fetch.mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({ status: 'error' }),
                ok: false,
            })
        );

        // Call addToFavorites with mocked showModalMessage
        await expect(addToFavorites(propertyId, app, mockShowModalMessage)).rejects.toThrow('Error adding property to favorites');

        // Verify showModalMessage was called with the error message
        expect(mockShowModalMessage).toHaveBeenCalledWith('An error occurred. Please try again.');
    });
});