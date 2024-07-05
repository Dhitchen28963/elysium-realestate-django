document.addEventListener('DOMContentLoaded', function () {
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

        closeModal.onclick = function () {
            modal.style.display = 'none';
        };

        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };
    }

    // Toggle favorite status
    async function toggleFavorite(propertyId, isFavorite, app) {
        const url = isFavorite ?
            `/${app}/remove-from-favorites/${propertyId}/` :
            `/${app}/add-to-favorites/${propertyId}/`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({})
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

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
        } catch (error) {
            console.error('Error:', error.message);
            showModalMessage('An error occurred. Please try again.');
        }
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
    async function requestCustomViewing(propertyId) {
        const customViewingForm = document.getElementById('custom-viewing-form');
        const formData = new FormData(customViewingForm);

        try {
            const response = await fetch(`/real_estate/request_custom_viewing/${propertyId}/`, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            if (data.status === 'ok') {
                showModalMessage('Viewing request sent to the agent!');
                const modal = document.getElementById("viewingModal");
                modal.style.display = "none";
            } else {
                showModalMessage('Error sending viewing request: ' + JSON.stringify(data.errors));
            }
        } catch (error) {
            console.error('Error:', error);
            showModalMessage('An error occurred. Please try again.');
        }
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
        button.addEventListener('click', function (event) {
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
        button.addEventListener('click', function () {
            const propertyId = this.getAttribute('data-property-id');
            const app = this.getAttribute('data-app');
            removeFromFavorites(propertyId, app);
        });
    });

    // Event listener for custom viewing request
    const customViewingForm = document.getElementById('custom-viewing-form');
    if (customViewingForm) {
        customViewingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const propertyId = customViewingForm.getAttribute('data-property-id');
            requestCustomViewing(propertyId);
        });
    }

    // Event listener for contact form submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const propertyId = contactForm.getAttribute('data-property-id');
            const app = contactForm.getAttribute('data-app');
            contactAgent(propertyId, app);
        });
    }

    // Event listener for favorites star button
    const favoritesStarButtons = document.querySelectorAll('.favorites-star');
    favoritesStarButtons.forEach(button => {
        button.addEventListener('click', function (event) {
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
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            const button = this.querySelector('button.favorites-star');
            if (button) {
                button.click();
            }
        });
    });

    // Modal handling for schedule viewing
    const viewingModal = document.getElementById("viewingModal");
    const closeViewingModal = document.getElementsByClassName("close")[0];

    document.querySelectorAll('.open-modal').forEach(button => {
        button.addEventListener('click', function () {
            const propertyId = this.getAttribute('data-property-id');
            const form = document.getElementById('custom-viewing-form');
            form.setAttribute('action', `/real_estate/request_custom_viewing/${propertyId}/`);
            form.setAttribute('data-property-id', propertyId);
            viewingModal.style.display = 'block';
        });
    });

    if (closeViewingModal) {
        closeViewingModal.addEventListener('click', function () {
            viewingModal.style.display = 'none';
        });
    }

    window.addEventListener('click', function (event) {
        if (event.target == viewingModal) {
            viewingModal.style.display = 'none';
        }
    });

    // My Account Sidebar Handling
    const myAccountBtn = document.getElementById('my-account-btn');
    const sidebar = document.getElementById('my-account-sidebar');
    const userIcon = document.getElementById('user-icon');

    function toggleSidebar(event) {
        event.preventDefault();
        sidebar.style.display = 'block';
    }

    if (myAccountBtn && sidebar) {
        myAccountBtn.addEventListener('click', toggleSidebar);
    }

    if (userIcon && sidebar) {
        userIcon.addEventListener('click', toggleSidebar);
    }

    // Close the sidebar if clicking outside of it
    window.addEventListener('click', function (event) {
        if (event.target !== sidebar && event.target !== myAccountBtn && event.target !== userIcon && !sidebar.contains(event.target)) {
            sidebar.style.display = 'none';
        }
    });

    // Close sidebar function
    function closeSidebar() {
        sidebar.style.display = 'none';
    }

    // Event listener for close sidebar button
    const closeSidebarButton = document.getElementById('close-sidebar');
    if (closeSidebarButton) {
        closeSidebarButton.addEventListener('click', closeSidebar);
    }

    // Additional custom viewing request handling
    const form = document.getElementById('custom-viewing-form');
    if (form) {
        form.addEventListener('submit', function (event) {
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
            if (filtersContainer.style.display === 'none') {
                filtersContainer.style.display = 'block';
                toggleButton.textContent = 'Hide Filters';
            } else {
                filtersContainer.style.display = 'none';
                toggleButton.textContent = 'Show Filters';
            }
        });
    }

    // Ensure the filters container is hidden on page load
    if (filtersContainer) {
        filtersContainer.style.display = 'none';
    }

    // Event listener for Buy and Rent buttons
    const buyButton = document.getElementById('buy-button');
    const rentButton = document.getElementById('rent-button');
    const homeSearchInput = document.getElementById('home-search-input');

    if (buyButton && rentButton) {
        buyButton.addEventListener('click', function (event) {
            const screenWidth = window.innerWidth;
            if (screenWidth <= 693) {
                window.location.href = "/real_estate/property-sale/";
            } else {
                const searchValue = homeSearchInput.value.trim();
                const queryParams = new URLSearchParams(new FormData(document.getElementById('home-search-form')));

                if (searchValue && searchValue.toLowerCase() !== 'none') {
                    window.location.href = `/real_estate/property-sale/?${queryParams.toString()}`;
                } else {
                    alert('Please enter a location');
                }
            }
        });

        rentButton.addEventListener('click', function (event) {
            const screenWidth = window.innerWidth;
            if (screenWidth <= 693) {
                window.location.href = "/real_estate/property-rent/";
            } else {
                const searchValue = homeSearchInput.value.trim();
                const queryParams = new URLSearchParams(new FormData(document.getElementById('home-search-form')));

                if (searchValue && searchValue.toLowerCase() !== 'none') {
                    window.location.href = `/real_estate/property-rent/?${queryParams.toString()}`;
                } else {
                    alert('Please enter a location');
                }
            }
        });
    }

    // Event listener for Student Accommodation search button
    const studentSearchButton = document.querySelector('#student-search-form button[type="submit"]');
    const studentSearchInput = document.querySelector('#student-search-form input[name="search"]');

    if (studentSearchButton && studentSearchInput) {
        studentSearchButton.addEventListener('click', function (event) {
            if (studentSearchInput.value.trim() === '') {
                alert('Please enter a location');
                event.preventDefault();
            }
        });
    }

    // Ensure filters are visible before form submission
    const studentSearchForm = document.getElementById('student-search-form');
    if (studentSearchForm) {
        studentSearchForm.addEventListener('submit', function (event) {
            if (filtersContainer.style.display === 'none') {
                filtersContainer.style.display = 'block';
            }
        });
    }

    // Dropdown menu handling
    const menuItems = document.querySelectorAll('.menu > li');

    menuItems.forEach(item => {
        item.addEventListener('mouseover', function () {
            this.classList.add('active');
        });

        item.addEventListener('mouseout', function () {
            this.classList.remove('active');
        });

        item.addEventListener('click', function (e) {
            if (!e.target.closest('a')) {
                e.preventDefault();
            }
            this.classList.toggle('active');
        });
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.menu')) {
            menuItems.forEach(item => {
                item.classList.remove('active');
            });
        }
    });

    // Carousel and thumbnail handling
    const carouselContainer = document.querySelector('.carousel-container');
    const carousel = document.querySelector('.carousel');
    const prevButton = document.querySelector('.carousel-control-prev');
    const nextButton = document.querySelector('.carousel-control-next');
    const thumbnails = document.querySelectorAll('.thumbnail-item img');

    let currentIndex = 0;

    function updateCarousel() {
        if (carouselContainer && carousel) {
            const width = carouselContainer.clientWidth;
            carousel.style.transform = `translateX(-${currentIndex * width}px)`;
        } else {
            console.error('Carousel or carousel container element not found.');
        }
    }

    function setActiveThumbnail(index) {
        thumbnails.forEach((thumbnail, i) => {
            if (i === index) {
                thumbnail.classList.add('active');
            } else {
                thumbnail.classList.remove('active');
            }
        });
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', function () {
            currentIndex = (currentIndex > 0) ? currentIndex - 1 : carousel.children.length - 1;
            updateCarousel();
            setActiveThumbnail(currentIndex);
        });

        nextButton.addEventListener('click', function () {
            currentIndex = (currentIndex < carousel.children.length - 1) ? currentIndex + 1 : 0;
            updateCarousel();
            setActiveThumbnail(currentIndex);
        });
    }

    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function () {
            currentIndex = index;
            updateCarousel();
            setActiveThumbnail(currentIndex);
        });
    });

    window.addEventListener('resize', updateCarousel);
    updateCarousel();
    setActiveThumbnail(currentIndex);
});