const addToFavorites = require('./addToFavorites');
const closeSidebar = require('./closeSidebar').closeSidebar;
const clearModalMessages = require('./clearModalMessages');
const removeFromFavorites = require('./removeFromFavorites');
const requestCustomViewing = require('./requestCustomViewing');
const showModalMessage = require('./showModalMessage');
const validateDate = require('./validateDate');
const { toggleFavorite } = require('./toggleFavorite');

function setupEventListeners() {
    const customViewingForm = document.getElementById('custom-viewing-form');
    if (customViewingForm) {
        customViewingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            clearModalMessages();
            const propertyId = customViewingForm.getAttribute('data-property-id');
            requestCustomViewing(propertyId);
        });
    }

    const addToFavoritesButtons = document.querySelectorAll('.property-actions[data-action="addToFavorites"]');
    addToFavoritesButtons.forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();
            const propertyId = button.getAttribute('data-property-id');
            const app = button.getAttribute('data-app');
            try {
                await addToFavorites(propertyId, app, showModalMessage);
                showModalMessage('Property added to favorites');
            } catch (error) {
                if (error.message === 'exists') {
                    showModalMessage('Property is already in favorites.');
                } else {
                    showModalMessage('Error adding property to favorites.');
                }
            }
        });
    });

    const removeFavoriteButtons = document.querySelectorAll('.remove-favorite-btn');
    removeFavoriteButtons.forEach(button => {
        button.addEventListener('click', async function(event) {
            event.preventDefault();
            const propertyId = button.getAttribute('data-property-id');
            const app = button.getAttribute('data-app');
            try {
                await removeFromFavorites(propertyId, app);
                showModalMessage('Property removed from favorites');
            } catch (error) {
                showModalMessage('Error removing property from favorites.');
            }
        });
    });

    const closeSidebarButton = document.getElementById('close-sidebar');
    if (closeSidebarButton) {
        closeSidebarButton.addEventListener('click', function(event) {
            event.preventDefault();
            closeSidebar();
        });
    }

    const preferredDateInput = document.getElementById('preferred_date');
    if (preferredDateInput) {
        preferredDateInput.addEventListener('change', function(event) {
            validateDate();
        });
    }

    const updateViewingForm = document.getElementById('update-viewing-form');
    if (updateViewingForm) {
        updateViewingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            clearModalMessages();
            if (!validateDate()) {
                return;
            }
            showModalMessage('Viewing updated successfully!');
        });
    }

    const studentSearchButton = document.getElementById('student-search-form');
    if (studentSearchButton) {
        studentSearchButton.addEventListener('click', function(event) {
            const studentSearchInput = document.getElementById('student-search-input');
            if (!studentSearchInput || !studentSearchInput.value.trim()) {
                event.preventDefault();
                alert('Please enter a location');
                displayNoPropertiesFound('No student accommodations found.');
            }
        });
    }

    const landSearchButton = document.getElementById('land-search-form');
    if (landSearchButton) {
        landSearchButton.addEventListener('click', function(event) {
            const landSearchInput = document.getElementById('land-search-input');
            if (!landSearchInput || !landSearchInput.value.trim()) {
                event.preventDefault();
                alert('Please enter a location');
                displayNoPropertiesFound('No land available for sale at the moment. Please use the search bar above to find properties.');
            }
        });
    }

    const rentSearchButton = document.getElementById('rent-button');
    if (rentSearchButton) {
        rentSearchButton.addEventListener('click', function(event) {
            const rentSearchInput = document.getElementById('home-search-input');
            if (!rentSearchInput || !rentSearchInput.value.trim()) {
                event.preventDefault();
                alert('Please enter a location');
                displayNoPropertiesFound('No properties found for rent. Please use the search bar above to find properties.');
            }
        });
    }

    const buySearchButton = document.getElementById('buy-button');
    if (buySearchButton) {
        buySearchButton.addEventListener('click', function(event) {
            const buySearchInput = document.getElementById('home-search-input');
            if (!buySearchInput || !buySearchInput.value.trim()) {
                event.preventDefault();
                alert('Please enter a location');
                displayNoPropertiesFound('No properties found for sale. Please use the search bar above to find properties.');
            }
        });
    }

    const favoritesStarButton = document.querySelector('.favorites-star');
    if (favoritesStarButton) {
        favoritesStarButton.addEventListener('click', function(event) {
            toggleFavorite();
        });
    }
}

function displayNoPropertiesFound(message) {
    const noPropertiesFound = document.createElement('p');
    noPropertiesFound.className = 'no-properties-found';
    noPropertiesFound.textContent = message;
    document.body.appendChild(noPropertiesFound);
}

module.exports = { setupEventListeners };