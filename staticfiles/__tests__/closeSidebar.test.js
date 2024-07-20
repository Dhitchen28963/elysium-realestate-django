const { setupEventListeners } = require('../../static/js/functions/setupEventListeners');
const addToFavorites = require('../../static/js/functions/addToFavorites');
const { closeSidebar } = require('../../static/js/functions/closeSidebar');
const clearModalMessages = require('../../static/js/functions/clearModalMessages');
const removeFromFavorites = require('../../static/js/functions/removeFromFavorites');
const requestCustomViewing = require('../../static/js/functions/requestCustomViewing');
const showModalMessage = require('../../static/js/functions/showModalMessage');
const validateDate = require('../../static/js/functions/validateDate');
const getCSRFToken = require('../../static/js/functions/getCSRFToken');

jest.mock('../../static/js/functions/addToFavorites');
jest.mock('../../static/js/functions/closeSidebar', () => ({ closeSidebar: jest.fn() }));
jest.mock('../../static/js/functions/clearModalMessages');
jest.mock('../../static/js/functions/removeFromFavorites');
jest.mock('../../static/js/functions/requestCustomViewing');
jest.mock('../../static/js/functions/showModalMessage');
jest.mock('../../static/js/functions/validateDate');
jest.mock('../../static/js/functions/getCSRFToken');

describe('setupEventListeners', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <form id="custom-viewing-form" data-property-id="1"></form>
            <button class="property-actions" data-action="addToFavorites" data-property-id="1" data-app="real_estate"></button>
            <button class="remove-favorite-btn" data-property-id="1" data-app="real_estate"></button>
            <button id="close-sidebar"></button>
            <form id="student-search-form">
                <input name="search" />
                <button type="submit">Search</button>
            </form>
            <input id="preferred_date" />
            <form id="update-viewing-form" action="/update-viewing/"></form>
        `;

        // Mock window.alert
        window.alert = jest.fn();

        setupEventListeners();
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('should call requestCustomViewing when custom viewing form is submitted', () => {
        const form = document.getElementById('custom-viewing-form');
        form.dispatchEvent(new Event('submit', { bubbles: true }));
        expect(requestCustomViewing).toHaveBeenCalledWith('1');
    });

    test('should call addToFavorites when property action button is clicked', () => {
        const button = document.querySelector('.property-actions[data-action="addToFavorites"]');
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(addToFavorites).toHaveBeenCalledWith('1', 'real_estate', showModalMessage);
    });

    test('should call removeFromFavorites when remove favorite button is clicked', () => {
        const button = document.querySelector('.remove-favorite-btn');
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(removeFromFavorites).toHaveBeenCalledWith('1', 'real_estate');
    });

    test('should call closeSidebar when close sidebar button is clicked', () => {
        const button = document.getElementById('close-sidebar');
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(closeSidebar).toHaveBeenCalled();
    });

    test('should call validateDate when preferred date input is changed', () => {
        const input = document.getElementById('preferred_date');
        input.dispatchEvent(new Event('change', { bubbles: true }));
        expect(validateDate).toHaveBeenCalled();
    });

    test('should call showModalMessage when update viewing form is submitted', async () => {
        validateDate.mockReturnValue(true);
        const form = document.getElementById('update-viewing-form');
        await form.dispatchEvent(new Event('submit', { bubbles: true }));
        expect(showModalMessage).toHaveBeenCalledWith('Viewing updated successfully!');
    });

    test('should call alert when student search button is clicked without input', () => {
        const button = document.querySelector('#student-search-form button[type="submit"]');
        const input = document.querySelector('#student-search-form input[name="search"]');
        input.value = '';
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(window.alert).toHaveBeenCalledWith('Please enter a location');
    });
});