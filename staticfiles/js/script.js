document.addEventListener('DOMContentLoaded', function() {
    // Function to get CSRF Token
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to show modal message
    function showModalMessage(message) {
        const modal = document.getElementById('messageModal');
        const modalMessage = document.getElementById('modalMessage');
        const closeModal = document.getElementsByClassName('close')[0];

        modalMessage.textContent = message;
        modal.style.display = 'block';

        closeModal.onclick = function() {
            modal.style.display = 'none';
        };

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };
    }

    // Toggle favorite status
    function toggleFavorite(propertyId, isFavorite, app) {
        const url = isFavorite
            ? `/${app}/remove-from-favorites/${propertyId}/`
            : `/${app}/add-to-favorites/${propertyId}/`;
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                showModalMessage(isFavorite ? 'Property removed from favorites' : 'Property added to favorites');
                location.reload();
            } else if (data.status === 'exists') {
                showModalMessage('Property is already in favorites.');
                const button = document.querySelector(`.favorites-star[data-property-id="${propertyId}"]`);
                if (button) {
                    button.innerHTML = '<i class="fa-solid fa-star"></i> Remove from Favorites';
                    button.setAttribute('data-is-favorite', 'true');
                }
            } else {
                showModalMessage('Error updating favorites');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModalMessage('An error occurred. Please try again.');
        });
    }

    // Add to favorites
    function addToFavorites(propertyId, app) {
        fetch(`/${app}/add-to-favorites/${propertyId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                showModalMessage('Property added to favorites!');
                location.reload();
            } else if (data.status === 'exists') {
                showModalMessage('Property is already in favorites.');
                const button = document.querySelector(`.favorites-star[data-property-id="${propertyId}"]`);
                if (button) {
                    button.innerHTML = '<i class="fa-solid fa-star"></i> Remove from Favorites';
                    button.setAttribute('data-is-favorite', 'true');
                }
            } else {
                showModalMessage('Error adding property to favorites.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModalMessage('An error occurred. Please try again.');
        });
    }

    // Remove from favorites
    function removeFromFavorites(propertyId, app) {
        fetch(`/${app}/remove-from-favorites/${propertyId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'ok') {
                showModalMessage('Property removed from favorites!');
                location.reload();
            } else {
                showModalMessage('Error removing property from favorites.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModalMessage('An error occurred. Please try again.');
        });
    }

    // Request custom viewing
    function requestCustomViewing(propertyId, app) {
        const customViewingForm = document.getElementById('custom-viewing-form');
        const formData = new FormData(customViewingForm);

        fetch(customViewingForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                showModalMessage('Viewing request sent to the agent!');
                const modal = document.getElementById("viewingModal");
                modal.style.display = "none";
            } else {
                showModalMessage('Error sending viewing request: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModalMessage('An error occurred. Please try again.');
        });
    }

    // Contact agent
    function contactAgent(propertyId, app) {
        const contactForm = document.getElementById('contact-form');
        const formData = new FormData(contactForm);

        fetch(contactForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'message sent') {
                showModalMessage('Message sent to the agent!');
            } else {
                showModalMessage('Error sending message.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModalMessage('An error occurred. Please try again.');
        });
    }

    // Event listener for add to favorites
    document.querySelectorAll('.property-actions button[data-action]').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const propertyId = this.getAttribute('data-property-id');
            const action = this.getAttribute('data-action');
            const app = this.getAttribute('data-app');

            if (action === 'addToFavorites') {
                addToFavorites(propertyId, app);
            } else if (action === 'removeFromFavorites') {
                removeFromFavorites(propertyId, app);
            }
        });
    });

    // Event listener for removing from favorites
    document.querySelectorAll('.remove-favorite-btn').forEach(button => {
        button.addEventListener('click', function() {
            const propertyId = this.getAttribute('data-property-id');
            const app = this.getAttribute('data-app');
            removeFromFavorites(propertyId, app);
        });
    });

    // Event listener for custom viewing request
    const customViewingForm = document.getElementById('custom-viewing-form');
    if (customViewingForm) {
        customViewingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const propertyId = customViewingForm.getAttribute('data-property-id');
            const app = customViewingForm.getAttribute('data-app');
            requestCustomViewing(propertyId, app);
        });
    }

    // Event listener for contact form submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const propertyId = contactForm.getAttribute('data-property-id');
            const app = contactForm.getAttribute('data-app');
            contactAgent(propertyId, app);
        });
    }

    // Event listener for favorites star button
    const favoritesStarButtons = document.querySelectorAll('.favorites-star');
    favoritesStarButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const propertyId = this.getAttribute('data-property-id');
            const isFavorite = this.getAttribute('data-is-favorite') === 'true';
            const app = this.getAttribute('data-app');

            toggleFavorite(propertyId, isFavorite, app);
        });
    });

    // Event listener for forms to prevent default submission
    const favoriteForms = document.querySelectorAll('form[action*="add-to-favorites"], form[action*="remove-from-favorites"]');
    favoriteForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const button = this.querySelector('button.favorites-star');
            if (button) {
                button.click();
            }
        });
    });

    // Modal handling
    const modal = document.getElementById("viewingModal");
    const closeModal = document.getElementsByClassName("close")[0];

    document.querySelectorAll('button[data-action="scheduleViewing"]').forEach(button => {
        button.addEventListener('click', function() {
            modal.style.display = "block";
        });
    });

    if (closeModal) {
        closeModal.addEventListener('click', function() {
            modal.style.display = "none";
        });
    }

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // My Account Sidebar Handling
    const myAccountBtn = document.getElementById('my-account-btn');
    const sidebar = document.getElementById('my-account-sidebar');

    if (myAccountBtn && sidebar) {
        myAccountBtn.addEventListener('click', function() {
            sidebar.style.display = 'block';
        });

        window.addEventListener('click', function(event) {
            if (event.target == sidebar) {
                sidebar.style.display = 'none';
            }
        });
    }

    // Additional custom viewing request handling
    const form = document.getElementById('custom-viewing-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const propertyId = form.getAttribute('data-property-id');
            const url = `/request-custom-viewing/${propertyId}/`;
            const formData = new FormData(form);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'ok') {
                    showModalMessage('Viewing request sent successfully.');
                    const modal = document.getElementById("viewingModal");
                    modal.style.display = "none";
                } else {
                    showModalMessage('Error sending viewing request: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showModalMessage('An error occurred. Please try again.');
            });
        });
    }

    // Toggle Filters
    const toggleButton = document.getElementById('toggle-filters');
    const filtersContainer = document.getElementById('filters-container');
    
    if (toggleButton && filtersContainer) {
        toggleButton.addEventListener('click', function() {
            if (filtersContainer.style.display === 'none' || filtersContainer.style.display === '') {
                filtersContainer.style.display = 'block';
                toggleButton.textContent = 'Hide Filters';
            } else {
                filtersContainer.style.display = 'none';
                toggleButton.textContent = 'Show Filters';
            }
        });
    }

    // Event listener for Buy and Rent buttons
    const buyButton = document.getElementById('buy-button');
    const rentButton = document.getElementById('rent-button');
    const searchInput = document.querySelector('input[name="search"]');

    if (buyButton && rentButton) {
        buyButton.addEventListener('click', function() {
            const searchValue = searchInput.value.trim();
            if (searchValue) {
                window.location.href = `/real_estate/property_sale/?search=${encodeURIComponent(searchValue)}`;
            } else {
                alert('Please enter a location');
            }
        });

        rentButton.addEventListener('click', function() {
            const searchValue = searchInput.value.trim();
            if (searchValue) {
                window.location.href = `/real_estate/property_rent/?search=${encodeURIComponent(searchValue)}`;
            } else {
                alert('Please enter a location');
            }
        });
    }
});
