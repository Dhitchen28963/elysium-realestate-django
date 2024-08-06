document.addEventListener('DOMContentLoaded', function () {
    // Function to handle collapsible content
    const collapsibles = document.querySelectorAll('.collapsible');
    collapsibles.forEach(collapsible => {
        collapsible.addEventListener('click', function () {
            this.classList.toggle('active');
            const content = this.nextElementSibling;
            if (content.style.display === 'block') {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }
        });
    });

    // Function to handle close button for collapsible content
    const closeButtons = document.querySelectorAll('.close-collapsible');
    closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const content = this.parentElement;
            content.style.display = 'none';
            const collapsible = content.previousElementSibling;
            if (collapsible.classList.contains('collapsible')) {
                collapsible.classList.remove('active');
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    });

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
        modalMessage.innerHTML = message;
        modal.style.display = 'block';
    }

    // Closing of modal message
    const closeModalButtons = document.querySelectorAll('.modal-content .close');
    closeModalButtons.forEach(button => {
        button.onclick = function () {
            button.parentElement.parentElement.style.display = 'none';
        };
    });

    window.onclick = function (event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
        }
    };

    // Edit comment handling
    document.querySelectorAll('button.edit-comment').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-id');
            const commentBodyElement = document.querySelector(`#comment-${commentId} .comment-body`);
            if (!commentBodyElement) {
                showModalMessage('Comment body not found.');
                return;
            }
            const commentBody = commentBodyElement.innerText;
            const editCommentBody = document.getElementById('editCommentBody');
            if (!editCommentBody) {
                showModalMessage('Edit comment body textarea not found.');
                return;
            }
            editCommentBody.value = commentBody;

            const editModal = document.getElementById('editModal');
            if (!editModal) {
                showModalMessage('Edit comment modal not found.');
                return;
            }
            editModal.style.display = 'block';

            const saveEditButton = document.getElementById('saveEdit');
            if (!saveEditButton) {
                showModalMessage('Save edit button not found.');
                return;
            }
            saveEditButton.onclick = function (event) {
                event.preventDefault();
                const newBody = editCommentBody.value;
                const urlPrefix = window.location.pathname.includes('faq') ? '/faq' : '/blog';

                fetch(`${urlPrefix}/comment/${commentId}/edit/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ body: newBody })
                }).then(response => response.json()).then(data => {
                    if (data.success) {
                        document.querySelector(`#comment-${commentId} .comment-body`).innerText = newBody;
                        editModal.style.display = 'none';
                        showModalMessage('Comment edited successfully.');
                    } else {
                        showModalMessage('Failed to edit comment.');
                    }
                }).catch(error => {
                    showModalMessage('An error occurred: ' + error.message);
                });
            };
        });
    });

    // Delete comment handling
    document.querySelectorAll('button.delete-comment').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-id');
            const deleteModal = document.getElementById('deleteModal');
            if (!deleteModal) {
                showModalMessage('Delete comment modal not found.');
                return;
            }
            deleteModal.style.display = 'block';

            const confirmDeleteButton = document.getElementById('confirmDelete');
            if (!confirmDeleteButton) {
                showModalMessage('Confirm delete button not found.');
                return;
            }
            confirmDeleteButton.onclick = function () {
                const urlPrefix = window.location.pathname.includes('faq') ? '/faq' : '/blog';

                fetch(`${urlPrefix}/comment/${commentId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(`comment-${commentId}`).remove();
                        deleteModal.style.display = 'none';
                        showModalMessage('Comment deleted successfully.');
                    } else {
                        showModalMessage('An error occurred: ' + data.error);
                    }
                })
                .catch(error => {
                    showModalMessage('An error occurred.');
                });
            };
        });
    });

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
    function validateDate(inputId) {
        const dateInput = document.getElementById(inputId);
        const currentDate = new Date();
        const selectedDate = new Date(dateInput.value);

        if (isNaN(selectedDate.getTime())) {
            showModalMessage('Please enter a valid date.');
            dateInput.value = '';  // Clear invalid date
            return false;
        }

        if (selectedDate < currentDate.setHours(0, 0, 0, 0)) {
            showModalMessage('You cannot select a past date. Please choose a valid date.');
            dateInput.value = '';  // Clear past date
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
            showModalMessage('An error occurred. Please try again.');
        });
    }

    // Remove
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
            showModalMessage('An error occurred. Please try again.');
        });
    }

    async function requestCustomViewing(propertyId) {
        const customViewingForm = document.getElementById('custom-viewing-form');
        const formData = new FormData(customViewingForm);

        if (!validateDate('preferred_date')) return;

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
            showModalMessage('An error occurred while sending the viewing request. Please try again.');
        } finally {
            const modal = document.getElementById("viewingModal");
            if (modal) {
                modal.style.display = "none";
            }
        }
    }

    // Function to request a slot viewing
    async function requestSlotViewing(slotId) {
        try {
            const name = document.getElementById('slot-name').value;
            const contact = document.getElementById('slot-contact').value;
            const email = document.getElementById('slot-email').value;

            const url = `/real_estate/book_viewing_slot/${slotId}/`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ name, contact, email })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            if (data.status === 'ok') {
                showModalMessage('Viewing slot booked successfully!');
            } else {
                throw new Error('Server returned an error: ' + JSON.stringify(data.errors));
            }
        } catch (error) {
            showModalMessage('An error occurred while booking the viewing slot. Please try again.');
        } finally {
            const modal = document.getElementById("viewingModal");
            if (modal) {
                modal.style.display = 'none';
            }
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

            if (!form) {
                return;
            }

            form.setAttribute('action', `/real_estate/request_custom_viewing/${propertyId}/`);
            form.setAttribute('data-property-id', propertyId);

            // Fetch available slots and display them in the modal
            fetch(`/real_estate/view_property_slots/${propertyId}/`)
                .then(response => response.json())
                .then(data => {
                    const slotsContainer = document.getElementById('available-slots-container');

                    if (!slotsContainer) {
                        return;
                    }

                    slotsContainer.innerHTML = '';

                    if (data.slots && data.slots.length > 0) {
                        data.slots.forEach(slot => {
                            const slotButton = document.createElement('button');
                            slotButton.textContent = `${slot.date} ${slot.start_time} - ${slot.end_time}`;
                            slotButton.onclick = () => {
                                const slotBookingForm = document.getElementById('slot-booking-form');
                                if (slotBookingForm) {
                                    slotBookingForm.style.display = 'block';
                                }
                                const bookSlotButton = document.getElementById('book-slot-button');
                                if (bookSlotButton) {
                                    bookSlotButton.onclick = () => requestSlotViewing(slot.id);
                                }
                            };
                            slotsContainer.appendChild(slotButton);
                        });
                    } else {
                        slotsContainer.innerHTML = '<p>No available slots</p>';
                    }
                })
                .catch(error => showModalMessage('Error fetching available slots'));

            const viewingModal = document.getElementById('viewingModal');

            if (viewingModal) {
                viewingModal.style.display = 'block';
            }
        });
    });

    // Event listener for booking viewing slot
    document.querySelectorAll('.book-viewing').forEach(button => {
        button.addEventListener('click', function () {
            const slotId = this.getAttribute('data-slot-id');
            requestSlotViewing(slotId);
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
                showModalMessage('An error occurred. Please try again.');
            });
        }
    });

    // Event listener for validating date
    const preferredDateInput = document.getElementById('preferred_date');
    if (preferredDateInput) {
        preferredDateInput.addEventListener('change', function () {
            validateDate('preferred_date');
        });
    }

    // Event listener for updating viewing
    document.querySelectorAll('.update-viewing-btn').forEach(button => {
        button.addEventListener('click', function () {
            const viewingId = this.getAttribute('data-viewing-id');
            const updateModal = document.getElementById('updateModal');
            const updateViewingForm = document.getElementById('updateViewingForm');
            const viewingIdInput = document.getElementById('viewingId');
            const updatePreferredDateInput = document.getElementById('preferredDate');

            // Set the form action URL and hidden input value
            updateViewingForm.setAttribute('data-viewing-id', viewingId);
            viewingIdInput.value = viewingId;

            // Display the modal
            updateModal.style.display = 'block';

            // Attach the validation function to the update date input
            updatePreferredDateInput.addEventListener('change', function () {
                validateDate('preferredDate');
            });
        });
    });

    const updateViewingForm = document.getElementById('updateViewingForm');
    if (updateViewingForm) {
        updateViewingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            clearModalMessages();  // Clear previous messages

            if (!validateDate('preferredDate')) {
                return;  // Prevent form submission if date is invalid
            }

            const viewingId = updateViewingForm.getAttribute('data-viewing-id');
            const url = `/real_estate/update_viewing/${viewingId}/`;
            const formData = new FormData(updateViewingForm);

            // Adding missing fields manually if they are not in the form already
            const contactInput = document.getElementById('contact');
            const emailInput = document.getElementById('email');
            const messageInput = document.getElementById('message');
            if (!formData.has('contact') && contactInput) formData.append('contact', contactInput.value);
            if (!formData.has('email') && emailInput) formData.append('email', emailInput.value);
            if (!formData.has('message') && messageInput) formData.append('message', messageInput.value);

            const formDataObject = Object.fromEntries(formData.entries());

            console.log(`Submitting form to URL: ${url}`);
            console.log('Form data:', formDataObject);

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
            })
            .then(response => {
                console.log(`Response status: ${response.status}`);
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(JSON.stringify(err));
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'ok') {
                    showModalMessage('Viewing updated successfully!');
                    const updateModal = document.getElementById('updateModal');
                    updateModal.style.display = 'none';
                    location.reload();
                } else {
                    showModalMessage(`Error updating viewing: ${JSON.stringify(data.errors)}`);
                }
            })
            .catch(error => {
                console.error(`Error occurred: ${error}`);
                showModalMessage(`An error occurred. Please try again. Details: ${error.message}`);
            });
        });
    }

    // Show modal message on specific actions
    function showConfirmationMessage(message) {
        showModalMessage(message);
    }

    // Comment form handling
    const commentForm = document.getElementById('commentForm');
    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(commentForm);
            fetch(commentForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showModalMessage('Comment has been submitted.');
                } else {
                    showModalMessage('Failed to submit comment.');
                }
            })
            .catch(error => {
                showModalMessage('An error occurred: ' + error.message);
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
    document.getElementById('resultBorrowAmount').innerText = borrowAmount.toFixed(2);
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
