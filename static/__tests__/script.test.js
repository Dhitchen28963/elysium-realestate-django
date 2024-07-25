/**
 * @jest-environment jsdom
 */

const {
    getCSRFToken,
    showModalMessage,
    clearModalMessages,
    validateContactNumber,
    validateDate,
    toggleFavorite,
    addToFavorites,
    removeFromFavorites,
    requestCustomViewing,
    requestSlotViewing,
    closeSidebar,
    nextStep,
    prevStep,
    updateTermValue,
    calculateMortgage,
    // Import other functions as needed
} = require('../js/functions/script');

describe('script.js functions', () => {
    beforeEach(() => {
        // Set up DOM elements
        document.body.innerHTML = `
            <div id="messageModal" style="display:none;">
                <p id="modalMessage"></p>
                <span class="close"></span>
            </div>
            <input id="preferred_date" type="date" />
            <form id="custom-viewing-form"></form>
            <div class="property-actions">
                <button data-action="addToFavorites" data-property-id="1" data-app="app"></button>
                <button data-action="removeFromFavorites" data-property-id="1" data-app="app"></button>
            </div>
            <div id="my-account-sidebar" style="display:none;"></div>
            <input id="propertyPrice" type="number" />
            <input id="deposit" type="number" />
            <input id="term" type="number" />
            <input id="interestRate" type="number" />
            <div id="result"></div>
            <div id="resultPropertyPriceInput"></div>
            <div id="resultDeposit"></div>
            <div id="resultTerm"></div>
            <div id="resultInterestRate"></div>
            <div id="resultBorrowAmount"></div>
            <div id="resultMonthlyRepayments"></div>
            <div id="resultTotalInterest"></div>
            <div id="resultTotalRepayable"></div>
            <div id="resultPropertyPrice"></div>
            <input id="slot-name" type="text" />
            <input id="slot-contact" type="text" />
            <input id="slot-email" type="email" />
            <!-- Add other necessary DOM elements -->
        `;
        
        // Mock location.reload
        delete window.location;
        window.location = { reload: jest.fn() };
    });

    test('getCSRFToken returns CSRF token from cookies', () => {
        document.cookie = 'csrftoken=testToken';
        expect(getCSRFToken()).toBe('testToken');
    });

    test('showModalMessage displays message in modal', () => {
        showModalMessage('Test Message');
        expect(document.getElementById('messageModal').style.display).toBe('block');
        expect(document.getElementById('modalMessage').textContent).toBe('Test Message');
    });

    test('clearModalMessages clears the modal message and hides the modal', () => {
        clearModalMessages();
        expect(document.getElementById('messageModal').style.display).toBe('none');
        expect(document.getElementById('modalMessage').textContent).toBe('');
    });

    test('validateContactNumber validates correct UK numbers', () => {
        expect(validateContactNumber('07123456789')).toBe(true);
        expect(validateContactNumber('01234567890')).toBe(true);
        expect(validateContactNumber('12345')).toBe(false);
        expect(validateContactNumber('abcdefg')).toBe(false);
    });

    test('validateDate validates dates correctly', () => {
        const input = document.getElementById('preferred_date');
        input.value = '2099-01-01';
        expect(validateDate()).toBe(true);

        input.value = '1999-01-01';
        expect(validateDate()).toBe(false);
    });

    test('addToFavorites function', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ status: 'ok' })
            })
        );

        await addToFavorites(1, 'app');
        expect(fetch).toHaveBeenCalledTimes(1);
    });

    test('removeFromFavorites function', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ status: 'ok' })
            })
        );

        await removeFromFavorites(1, 'app');
        expect(fetch).toHaveBeenCalledTimes(1);
    });

    test('requestCustomViewing function', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ status: 'ok' })
            })
        );

        document.getElementById('preferred_date').value = '2099-01-01';
        const form = document.getElementById('custom-viewing-form');
        form.setAttribute('data-property-id', '1');

        await requestCustomViewing(1);
        expect(fetch).toHaveBeenCalledTimes(1);
    });

    test('requestSlotViewing function', async () => {
        global.fetch = jest.fn(() =>
            Promise.resolve({
                ok: true,
                json: () => Promise.resolve({ status: 'ok' })
            })
        );

        document.getElementById('slot-name').value = 'John Doe';
        document.getElementById('slot-contact').value = '07123456789';
        document.getElementById('slot-email').value = 'john.doe@example.com';

        await requestSlotViewing(1);
        expect(fetch).toHaveBeenCalledTimes(1);
    });

    test('closeSidebar function', () => {
        document.getElementById('my-account-sidebar').style.display = 'block';
        closeSidebar();
        expect(document.getElementById('my-account-sidebar').style.display).toBe('none');
    });

    test('nextStep function', () => {
        document.body.innerHTML += '<div id="step1" class="active"></div><div id="step2"></div>';
        nextStep(1);
        expect(document.getElementById('step1').classList.contains('active')).toBe(false);
        expect(document.getElementById('step2').classList.contains('active')).toBe(true);
    });

    test('prevStep function', () => {
        document.body.innerHTML += '<div id="step1"></div><div id="step2" class="active"></div>';
        prevStep(2);
        expect(document.getElementById('step2').classList.contains('active')).toBe(false);
        expect(document.getElementById('step1').classList.contains('active')).toBe(true);
    });

    test('updateTermValue function', () => {
        document.body.innerHTML += '<div id="termValue"></div>';
        updateTermValue(20);
        expect(document.getElementById('termValue').innerText).toBe('20 years');
    });

    test('calculateMortgage function', () => {
        document.getElementById('propertyPrice').value = 100000;
        document.getElementById('deposit').value = 20000;
        document.getElementById('term').value = 30;
        document.getElementById('interestRate').value = 5;

        calculateMortgage();

        expect(document.getElementById('resultBorrowAmount').innerText).toBe('80000.00');
        expect(document.getElementById('resultMonthlyRepayments').innerText).toBe('429.46');
        expect(document.getElementById('resultTotalInterest').innerText).toBe('74604.63'); // Updated to match the new value
        expect(document.getElementById('resultTotalRepayable').innerText).toBe('154604.63'); // Updated to match the new value
    });

    afterEach(() => {
        // Clear mocks after each test
        jest.clearAllMocks();
    });
});
