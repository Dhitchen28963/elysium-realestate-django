const removeFromFavorites = require('../../static/js/functions/removeFromFavorites');

// Mock fetch API for testing purposes
global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ status: 'ok' }),
        ok: true,
    })
);

// Mock location.reload
delete global.location;
global.location = {
    reload: jest.fn(),
};

// Mock showModalMessage
jest.mock('../../static/js/functions/showModalMessage', () => jest.fn());

const showModalMessage = require('../../static/js/functions/showModalMessage');

// Test cases
describe('removeFromFavorites', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    test('should remove property from favorites successfully', async () => {
        const propertyId = 1;
        const app = 'real_estate';
        await expect(removeFromFavorites(propertyId, app)).resolves.toEqual(expect.objectContaining({
            status: 'ok'
        }));
        expect(showModalMessage).toHaveBeenCalledWith('Property removed from favorites!');
        expect(global.location.reload).toHaveBeenCalled();
    });

    test('should handle error removing property from favorites', async () => {
        const propertyId = 2;
        const app = 'real_estate';
        global.fetch.mockImplementationOnce(() =>
            Promise.resolve({
                json: () => Promise.resolve({ status: 'error' }),
                ok: false,
            })
        );

        await expect(removeFromFavorites(propertyId, app)).rejects.toThrow('An error occurred');
        expect(showModalMessage).toHaveBeenCalledWith('An error occurred. Please try again.');
    });
});