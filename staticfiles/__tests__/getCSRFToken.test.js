const getCSRFToken = require('../../static/js/functions/getCSRFToken');

// Mock document.cookie for testing purposes
describe('getCSRFToken', () => {
    beforeEach(() => {
        // Restore the default value of document.cookie before each test
        Object.defineProperty(document, 'cookie', {
            writable: true,
            value: 'csrftoken=testtoken; othercookie=othervalue',
        });
    });

    test('should return correct CSRF token from document.cookie', () => {
        expect(getCSRFToken()).toBe('testtoken');
    });

    test('should return null if no CSRF token found in document.cookie', () => {
        Object.defineProperty(document, 'cookie', { value: 'othercookie=othervalue' });
        expect(getCSRFToken()).toBeNull();
    });

    test('should return null if document.cookie is empty', () => {
        Object.defineProperty(document, 'cookie', { value: '' });
        expect(getCSRFToken()).toBeNull();
    });

    test('should return null if no matching cookie value', () => {
        Object.defineProperty(document, 'cookie', { value: 'othercookie=othervalue' });
        expect(getCSRFToken()).toBeNull();
    });
});