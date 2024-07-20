const { toggleFavorite } = require('../../static/js/functions/toggleFavorite');

jest.mock('../../static/js/functions/toggleFavorite', () => ({
    toggleFavorite: jest.fn()
}));

describe('toggleFavorite', () => {
    test('should call toggleFavorite with correct arguments', () => {
        toggleFavorite('1', false, 'real_estate');
        expect(toggleFavorite).toHaveBeenCalledWith('1', false, 'real_estate');
    });
});