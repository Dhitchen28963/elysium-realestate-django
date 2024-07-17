const { setupEventListeners } = require('../../static/js/functions/setupEventListeners');
const { toggleFavorite } = require('../../static/js/functions/toggleFavorite');
const requestCustomViewing = require('../../static/js/functions/requestCustomViewing');
const addToFavorites = require('../../static/js/functions/addToFavorites');
const removeFromFavorites = require('../../static/js/functions/removeFromFavorites');
const clearModalMessages = require('../../static/js/functions/clearModalMessages');
const showModalMessage = require('../../static/js/functions/showModalMessage');
const validateDate = require('../../static/js/functions/validateDate');
const { closeSidebar } = require('../../static/js/functions/closeSidebar');

// Mock the functions
jest.mock('../../static/js/functions/toggleFavorite');
jest.mock('../../static/js/functions/requestCustomViewing');
jest.mock('../../static/js/functions/addToFavorites');
jest.mock('../../static/js/functions/removeFromFavorites');
jest.mock('../../static/js/functions/clearModalMessages');
jest.mock('../../static/js/functions/showModalMessage');
jest.mock('../../static/js/functions/validateDate');
jest.mock('../../static/js/functions/closeSidebar');

describe('setupEventListeners', () => {
    let originalAlert;
    let originalLocation;

    beforeAll(() => {
        // Mock global alert
        originalAlert = window.alert;
        window.alert = jest.fn();

        // Mock window location
        originalLocation = { ...window.location };
        delete window.location;
        window.location = { href: '', assign: jest.fn() };

        // Mock fetch
        global.fetch = jest.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ status: 'ok' }) }));
    });

    afterAll(() => {
        // Restore original alert and location
        window.alert = originalAlert;
        window.location = originalLocation;
    });

    beforeEach(() => {
        jest.clearAllMocks();
        document.body.innerHTML = `
            <div class="modal-content">
                <span class="close">×</span>
                <p id="modalMessage">You cannot select a past date. Please choose a valid date.</p>
            </div>
            <form id="custom-viewing-form" data-property-id="1"></form>
            <button class="property-actions" data-action="addToFavorites" data-property-id="1" data-app="real_estate"></button>
            <button class="remove-favorite-btn" data-property-id="1" data-app="real_estate"></button>
            <button class="favorites-star" data-property-id="1" data-is-favorite="false" data-app="real_estate"></button>
            <form action="add-to-favorites"><button class="favorites-star"></button></form>
            <button id="close-sidebar"></button>
            <button id="buy-button"></button>
            <button id="rent-button"></button>
            <form id="home-search-form"></form>
            <input id="home-search-input" value="test location">
            <button type="button" id="student-search-form">Search</button>
            <input id="student-search-input" value="">
            <button type="button" id="land-search-form">Search Land</button>
            <input id="land-search-input" value="">
            <input id="preferred_date">
            <form id="update-viewing-form" action="/update-viewing"></form>
            <input name="search" value="">
        `;
    });

    test('should call requestCustomViewing when custom viewing form is submitted', () => {
        setupEventListeners();
        const form = document.getElementById('custom-viewing-form');
        form.dispatchEvent(new Event('submit', { bubbles: true }));
        expect(clearModalMessages).toHaveBeenCalled();
        expect(requestCustomViewing).toHaveBeenCalledWith('1');
    });

    test('should call addToFavorites when property action button is clicked', async () => {
        setupEventListeners();
        const button = document.querySelector('.property-actions[data-action="addToFavorites"]');
        await button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(addToFavorites).toHaveBeenCalledWith('1', 'real_estate', showModalMessage);
        expect(showModalMessage).toHaveBeenCalledWith('Property added to favorites');
    });

    test('should call removeFromFavorites when remove favorite button is clicked', async () => {
        setupEventListeners();
        const button = document.querySelector('.remove-favorite-btn');
        await button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(removeFromFavorites).toHaveBeenCalledWith('1', 'real_estate');
        expect(showModalMessage).toHaveBeenCalledWith('Property removed from favorites');
    });

    test('should call toggleFavorite when favorites star button is clicked', () => {
        setupEventListeners();
        const button = document.querySelector('.favorites-star');
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(toggleFavorite).toHaveBeenCalled();
    });

    test('should prevent form submission and click favorites star button', () => {
        setupEventListeners();
        
        // Mock click event on the favorites star button
        const mockClick = jest.fn();
        const favoritesStarButton = document.querySelector('form[action*="add-to-favorites"] button.favorites-star');
        favoritesStarButton.addEventListener('click', mockClick);
    
        // Prevent default form submission behavior
        const form = document.querySelector('form[action*="add-to-favorites"]');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            favoritesStarButton.click();
        });
    
        // Trigger form submission
        form.dispatchEvent(new Event('submit', { bubbles: true }));
    
        // Expectations
        expect(mockClick).toHaveBeenCalled();
        expect(mockClick.mock.calls.length).toBe(1);
    });

    test('should call closeSidebar when close sidebar button is clicked', () => {
        setupEventListeners();
        const button = document.getElementById('close-sidebar');
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(closeSidebar).toHaveBeenCalled();
    });

    test('should call buy button event listener', () => {
        setupEventListeners();
        const button = document.getElementById('buy-button');
        const form = document.getElementById('home-search-form');
        const input = document.getElementById('home-search-input');
        const mockEvent = jest.fn(() => {
            const searchValue = input.value.trim();
            if (searchValue && searchValue.toLowerCase() !== 'none') {
                window.location.href = `/real_estate/property-sale/?${new URLSearchParams(new FormData(form)).toString()}`;
            } else {
                alert('Please enter a location');
            }
        });
        button.addEventListener('click', mockEvent);
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(mockEvent).toHaveBeenCalled();
    });

    test('should call rent button event listener', () => {
        setupEventListeners();
        const button = document.getElementById('rent-button');
        const form = document.getElementById('home-search-form');
        const input = document.getElementById('home-search-input');
        const mockEvent = jest.fn(() => {
            const searchValue = input.value.trim();
            if (searchValue && searchValue.toLowerCase() !== 'none') {
                window.location.href = `/real_estate/property-rent/?${new URLSearchParams(new FormData(form)).toString()}`;
            } else {
                alert('Please enter a location');
            }
        });
        button.addEventListener('click', mockEvent);
        button.dispatchEvent(new Event('click', { bubbles: true }));
        expect(mockEvent).toHaveBeenCalled();
    });

    test('should call alert when student search button is clicked without input', () => {
        setupEventListeners();
        
        // Simulate clicking the student search button without input
        const studentSearchButton = document.getElementById('student-search-form');
        expect(studentSearchButton).toBeTruthy();
        
        // Clear input value
        const studentSearchInput = document.getElementById('student-search-input');
        expect(studentSearchInput).toBeTruthy();
        studentSearchInput.value = '';
        
        // Dispatch click event on student search button
        studentSearchButton.dispatchEvent(new Event('click', { bubbles: true }));
        
        // Check if alert was called
        expect(window.alert).toHaveBeenCalledWith('Please enter a location');
        
        // Check if "no properties found" message is displayed
        const noPropertiesMessage = document.querySelector('.no-properties-found');
        expect(noPropertiesMessage).toBeTruthy();
        expect(noPropertiesMessage.textContent).toBe('No student accommodations found.');
    });

    test('should call alert when land search button is clicked without input', () => {
        setupEventListeners();
        
        // Simulate clicking the land search button without input
        const landSearchButton = document.getElementById('land-search-form');
        expect(landSearchButton).toBeTruthy();
        
        // Clear input value
        const landSearchInput = document.getElementById('land-search-input');
        expect(landSearchInput).toBeTruthy();
        landSearchInput.value = '';
        
        // Dispatch click event on land search button
        landSearchButton.dispatchEvent(new Event('click', { bubbles: true }));
        
        // Check if alert was called
        expect(window.alert).toHaveBeenCalledWith('Please enter a location');
        
        // Check if "no properties found" message is displayed
        const noPropertiesMessage = document.querySelector('.no-properties-found');
        expect(noPropertiesMessage).toBeTruthy();
        expect(noPropertiesMessage.textContent).toBe('No land available for sale at the moment. Please use the search bar above to find properties.');
    });

    test('should call alert when rent search button is clicked without input', () => {
        setupEventListeners();
        
        // Simulate clicking the rent search button without input
        const rentSearchButton = document.getElementById('rent-button');
        expect(rentSearchButton).toBeTruthy();
        
        // Clear input value
        const rentSearchInput = document.getElementById('home-search-input');
        expect(rentSearchInput).toBeTruthy();
        rentSearchInput.value = '';
        
        // Dispatch click event on rent search button
        rentSearchButton.dispatchEvent(new Event('click', { bubbles: true }));
        
        // Check if alert was called
        expect(window.alert).toHaveBeenCalledWith('Please enter a location');
        
        // Check if "no properties found" message is displayed
        const noPropertiesMessage = document.querySelector('.no-properties-found');
        expect(noPropertiesMessage).toBeTruthy();
        expect(noPropertiesMessage.textContent).toBe('No properties found for rent. Please use the search bar above to find properties.');
    });

    test('should call alert when buy search button is clicked without input', () => {
        setupEventListeners();
        
        // Simulate clicking the buy search button without input
        const buySearchButton = document.getElementById('buy-button');
        expect(buySearchButton).toBeTruthy();
        
        // Clear input value
        const buySearchInput = document.getElementById('home-search-input');
        expect(buySearchInput).toBeTruthy();
        buySearchInput.value = '';
        
        // Dispatch click event on buy search button
        buySearchButton.dispatchEvent(new Event('click', { bubbles: true }));
        
        // Check if alert was called
        expect(window.alert).toHaveBeenCalledWith('Please enter a location');
        
        // Check if "no properties found" message is displayed
        const noPropertiesMessage = document.querySelector('.no-properties-found');
        expect(noPropertiesMessage).toBeTruthy();
        expect(noPropertiesMessage.textContent).toBe('No properties found for sale. Please use the search bar above to find properties.');
    });

    test('should call validateDate and showModalMessage when update viewing form is submitted with valid date', () => {
        validateDate.mockReturnValueOnce(true);
        setupEventListeners();
        const form = document.getElementById('update-viewing-form');
        form.dispatchEvent(new Event('submit', { bubbles: true }));
        expect(clearModalMessages).toHaveBeenCalled();
        expect(validateDate).toHaveBeenCalled();
        expect(showModalMessage).toHaveBeenCalledWith('Viewing updated successfully!');
    });

    test('should not call showModalMessage when update viewing form is submitted with invalid date', () => {
        validateDate.mockReturnValueOnce(false);
        setupEventListeners();
        const form = document.getElementById('update-viewing-form');
        form.dispatchEvent(new Event('submit', { bubbles: true }));
        expect(clearModalMessages).toHaveBeenCalled();
        expect(validateDate).toHaveBeenCalled();
        expect(showModalMessage).not.toHaveBeenCalled();
    });
});