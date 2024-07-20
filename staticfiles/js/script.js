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

    // Function to clear previous modal messages
    function clearModalMessages() {
        const modal = document.getElementById('messageModal');
        const modalMessage = document.getElementById('modalMessage');
        modalMessage.textContent = '';
        modal.style.display = 'none';
    }

    // Function to validate the contact number
    function validateContactNumber(contact) {
        const regex = /^(?:0(?:7\d{9}|(?:1|2|3)\d{8,9}))$/;
        return regex.test(contact);
    }

    // Function to validate the date
    function validateDate() {
        const preferredDateInput = document.getElementById('preferred_date');
        const currentDate = new Date();
        const selectedDate = new Date(preferredDateInput.value);

        if (isNaN(selectedDate.getTime())) {
            showModalMessage('Please enter a valid date.');
            preferredDateInput.value = '';  // Clear invalid date
            return false;
        }

        if (selectedDate < currentDate.setHours(0, 0, 0, 0)) {
            showModalMessage('You cannot select a past date. Please choose a valid date.');
            preferredDateInput.value = '';  // Clear past date
            return false;
        }

        return true;
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
                    button.innerHTML = '<i class="fa-solid fa-star"></i> Saved';
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

    // Save
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
                    button.innerHTML = '<i class="fa-solid fa-star"></i> Saved';
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

    // Saved
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

    async function requestCustomViewing(propertyId) {
        const customViewingForm = document.getElementById('custom-viewing-form');
        const formData = new FormData(customViewingForm);

        if (!validateDate()) {
            return;
        }

        try {
            const url = `/real_estate/request_custom_viewing/${propertyId}/`;
            const response = await fetch(url, {
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
            } else {
                throw new Error('Server returned an error: ' + JSON.stringify(data.errors));
            }
        } catch (error) {
            console.error('Error:', error);
            showModalMessage('An error occurred while sending the viewing request. Please try again.');
        } finally {
            const modal = document.getElementById("viewingModal");
            modal.style.display = "none";
        }
    }    

    // Check if user is logged in from the data attribute in the body tag
    const isUserLoggedIn = document.body.getAttribute('data-authenticated') === 'true';

    // Event listener for custom viewing request
    const customViewingForm = document.getElementById('custom-viewing-form');
    if (customViewingForm) {
        customViewingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            clearModalMessages();  // Clear previous messages

            const contactInput = document.getElementById('contact').value;
            if (!validateContactNumber(contactInput)) {
                showModalMessage('Please enter a valid UK mobile or landline number.');
                return;
            }

            const propertyId = customViewingForm.getAttribute('data-property-id');
            requestCustomViewing(propertyId);
        });
    }

    // Event listener for Save
    document.querySelectorAll('.property-actions button[data-action]').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const propertyId = this.getAttribute('data-property-id');
            const action = this.getAttribute('data-action');
            const app = this.getAttribute('data-app');

            if (!isUserLoggedIn) {
                showModalMessage('Please log in or create an account to save properties.');
                return;
            }

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

    // Event listener for favorites star button
    const favoritesStarButtons = document.querySelectorAll('.favorites-star');
    favoritesStarButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const propertyId = this.getAttribute('data-property-id');
            const isFavorite = this.getAttribute('data-is-favorite') === 'true';
            const app = this.getAttribute('data-app');

            if (!isUserLoggedIn) {
                showModalMessage('Please log in or create an account to save properties.');
                return;
            }

            toggleFavorite(propertyId, isFavorite, app);
        });
    });

    // Event listener for open-modal button
    const openModalButtons = document.querySelectorAll('.open-modal');
    openModalButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            if (!isUserLoggedIn) {
                showModalMessage('Please log in or create an account to schedule a viewing.');
                return;
            }
            const propertyId = this.getAttribute('data-property-id');
            const form = document.getElementById('custom-viewing-form');
            form.setAttribute('action', `/real_estate/request_custom_viewing/${propertyId}/`);
            form.setAttribute('data-property-id', propertyId);
            viewingModal.style.display = 'block';
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
    const largeImage = document.querySelector('.large-image img');
    const smallImages = document.querySelectorAll('.small-image-item img');
    const thumbnails = document.querySelectorAll('.thumbnail-item img');
    const prevButton = document.querySelector('.carousel-control-prev');
    const nextButton = document.querySelector('.carousel-control-next');
    let currentIndex = 0;

    function updateCarousel() {
        if (largeImage && thumbnails.length > 0) {
            largeImage.src = thumbnails[currentIndex].src;
            setActiveThumbnail(currentIndex);
            updateSmallImages();
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

    function updateSmallImages() {
        smallImages.forEach((smallImage, i) => {
            const index = (currentIndex + i + 1) % thumbnails.length;
            smallImage.src = thumbnails[index].src;
        });
    }

    if (prevButton && nextButton) {
        prevButton.addEventListener('click', function () {
            currentIndex = (currentIndex > 0) ? currentIndex - 1 : thumbnails.length - 1;
            updateCarousel();
        });

        nextButton.addEventListener('click', function () {
            currentIndex = (currentIndex < thumbnails.length - 1) ? currentIndex + 1 : 0;
            updateCarousel();
        });
    }

    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function () {
            currentIndex = index;
            updateCarousel();
        });
    });

    updateCarousel();
    setActiveThumbnail(currentIndex);

    // Delete Confirmation Modal for Pending Viewings
    const deleteModal = document.getElementById('deleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    let viewingIdToDelete = null;

    document.querySelectorAll('.delete-viewing-btn').forEach(button => {
        button.addEventListener('click', function () {
            viewingIdToDelete = this.getAttribute('data-viewing-id');
            deleteModal.style.display = 'block';
        });
    });

    document.querySelector('.close').addEventListener('click', function () {
        deleteModal.style.display = 'none';
    });

    document.getElementById('cancelDelete').addEventListener('click', function () {
        deleteModal.style.display = 'none';
    });

    confirmDeleteBtn.addEventListener('click', function () {
        if (viewingIdToDelete) {
            fetch(`/real_estate/delete_viewing/${viewingIdToDelete}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({})
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'ok') {
                    showModalMessage('Viewing request deleted successfully.');
                    location.reload();
                } else {
                    showModalMessage('Error deleting viewing request.');
                }
                deleteModal.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                showModalMessage('An error occurred. Please try again.');
            });
        }
    });

    // Event listener for validating date
    const preferredDateInput = document.getElementById('preferred_date');
    if (preferredDateInput) {
        preferredDateInput.addEventListener('change', validateDate);
    }

    // Event listener for updating viewing
    const updateViewingForm = document.getElementById('update-viewing-form');
    if (updateViewingForm) {
        updateViewingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            clearModalMessages();  // Clear previous messages

            if (!validateDate()) {
                return;  // Prevent form submission if date is invalid
            }

            const url = updateViewingForm.getAttribute('action');
            const formData = new FormData(updateViewingForm);

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
                    showModalMessage('Viewing updated successfully!');
                } else {
                    showModalMessage('Error updating viewing: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showModalMessage('An error occurred. Please try again.');
            });
        });
    }
});

// Mortgage calculation
function nextStep(step) {
    document.getElementById(`step${step}`).classList.remove('active');
    document.getElementById(`step${step + 1}`).classList.add('active');
}

function prevStep(step) {
    document.getElementById(`step${step}`).classList.remove('active');
    document.getElementById(`step${step - 1}`).classList.add('active');
}

function updateTermValue(value) {
    document.getElementById('termValue').innerText = `${value} years`;
}

function calculateMortgage() {
    const propertyPrice = parseFloat(document.getElementById('propertyPrice').value);
    const deposit = parseFloat(document.getElementById('deposit').value);
    const term = parseInt(document.getElementById('term').value);
    const interestRate = parseFloat(document.getElementById('interestRate').value);

    const borrowAmount = propertyPrice - deposit; // Amount that can be borrowed
    const monthlyInterestRate = (interestRate / 100) / 12;
    const numberOfPayments = term * 12;
    const principal = borrowAmount;

    const monthlyRepayments = (principal * monthlyInterestRate) / (1 - Math.pow((1 + monthlyInterestRate), -numberOfPayments));
    const totalRepayable = monthlyRepayments * numberOfPayments;
    const totalInterest = totalRepayable - principal;

    document.getElementById('resultPropertyPriceInput').innerText = propertyPrice.toFixed(2);
    document.getElementById('resultDeposit').innerText = deposit.toFixed(2);
    document.getElementById('resultTerm').innerText = term;
    document.getElementById('resultInterestRate').innerText = interestRate.toFixed(2);
    document.getElementById('resultBorrowAmount').innerText = borrowAmount.toFixed(2); // Amount that can be borrowed
    document.getElementById('resultMonthlyRepayments').innerText = monthlyRepayments.toFixed(2);
    document.getElementById('resultTotalInterest').innerText = totalInterest.toFixed(2);
    document.getElementById('resultTotalRepayable').innerText = totalRepayable.toFixed(2);
    document.getElementById('resultPropertyPrice').innerText = propertyPrice.toFixed(2);

    document.getElementById('result').classList.add('active');
}

// Ensure these functions are accessible in the global scope
window.nextStep = nextStep;
window.prevStep = prevStep;
window.updateTermValue = updateTermValue;
window.calculateMortgage = calculateMortgage;