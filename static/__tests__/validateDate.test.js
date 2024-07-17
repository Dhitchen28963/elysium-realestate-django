// Import the function to be tested
const validateDate = require('../../static/js/functions/validateDate');

// Mock showModalMessage to prevent actual DOM manipulation during testing
jest.mock('../../static/js/functions/showModalMessage', () => jest.fn());

// Mock DOM elements for testing purposes
document.body.innerHTML = `
<input type="date" id="preferred_date" />
<div id="messageModal">
    <div id="modalMessage">Test Message</div>
</div>
`;

describe('validateDate', () => {
    test('should return true for valid future date', () => {
        const validDate = new Date(Date.now() + 86400000); // Tomorrow
        document.getElementById('preferred_date').value = validDate.toISOString().split('T')[0]; // Set date input value
        expect(validateDate()).toBe(true);
    });

    test('should return false for past date', () => {
        const pastDate = new Date(Date.now() - 86400000); // Yesterday
        document.getElementById('preferred_date').value = pastDate.toISOString().split('T')[0]; // Set date input value
        expect(validateDate()).toBe(false);
    });

    test('should return false for invalid date format', () => {
        document.getElementById('preferred_date').value = '2024-07-32'; // Invalid date
        expect(validateDate()).toBe(false);
    });
});