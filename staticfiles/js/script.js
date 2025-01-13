/* jshint esversion: 8 */

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

    // Account settings scroll to sections
    const links = document.querySelectorAll(".account-menu-link");
    links.forEach(link => {
        link.addEventListener("click", function (event) {
            // Prevent default behavior only if the link is not the first one (Account Settings)
            if (this.getAttribute("href") !== "#personal-details") {
                event.preventDefault();
                const targetId = this.getAttribute("href").substring(1);
                const targetElement = document.getElementById(targetId);
                const headerOffset = 110;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // Edit comment handling
    document.querySelectorAll('button.edit-comment').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const commentId = this.getAttribute('data-id');
            const commentBody = this.getAttribute('data-body');
            
            // Get modal elements
            const editModal = document.getElementById('editModal');
            const commentBodyTextarea = document.getElementById('commentBody');
            const editCommentForm = document.getElementById('editCommentForm');
            const commentIdInput = document.getElementById('commentId');

            // Check if all required elements exist
            if (!editModal || !commentBodyTextarea || !editCommentForm || !commentIdInput) {
                showModalMessage('Required form elements not found.');
                return;
            }

            // Set values
            commentBodyTextarea.value = commentBody;
            commentIdInput.value = commentId;
            
            // Show modal
            editModal.style.display = 'block';

            // Close button functionality
            const closeButtons = editModal.querySelectorAll('.close');
            closeButtons.forEach(button => {
                button.addEventListener('click', function() {
                    editModal.style.display = 'none';
                });
            });

            // Handle form submission
            editCommentForm.onsubmit = function(e) {
                e.preventDefault();
                const isFAQ = window.location.pathname.includes('faq');
                // Use appropriate URL format based on whether we're on FAQ or blog
                const url = isFAQ ? 
                    `/faq/comment/${commentId}/edit/` : 
                    `/blog/comment/edit/${commentId}/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        body: commentBodyTextarea.value
                    })
                })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => {
                            console.error('Server response:', text);
                            throw new Error('Server response not OK');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        showModalMessage('Comment updated successfully.');
                        setTimeout(() => {
                            location.reload();
                        }, 1500);
                    } else {
                        showModalMessage(data.error || 'Failed to update comment.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showModalMessage('An error occurred while updating the comment.');
                });
            };
        });
    });

    // Single global event listener for closing modals when clicking outside
    window.addEventListener('click', function(event) {
        const editModal = document.getElementById('editModal');
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
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
                const isFAQ = window.location.pathname.includes('faq');
                // Use appropriate URL format based on whether we're on FAQ or blog
                const url = isFAQ ? 
                    `/faq/comment/${commentId}/delete/` : 
                    `/blog/comment/delete/${commentId}/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken(),
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
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
                    console.error('Error:', error);
                    showModalMessage('An error occurred while deleting the comment.');
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

    // Check if user is logged in from the data attribute in the body tag
    const isUserLoggedIn = document.body.getAttribute('data-authenticated') === 'true';

    // Function to fetch and display available slots
    async function fetchAndDisplaySlots(propertyId) {
        try {
            const response = await fetch(`/real_estate/view_property_slots/${propertyId}/`);
            const data = await response.json();
            const slotsContainer = document.getElementById('available-slots-container');

            if (!slotsContainer) {
                console.error('Slots container not found');
                return;
            }

            slotsContainer.innerHTML = ''; // Clear existing content

            if (data.slots && data.slots.length > 0) {
                const slotsWrapper = document.createElement('div');
                slotsWrapper.className = 'slots-wrapper';

                data.slots.forEach(slot => {
                    // Create slot button
                    const slotButton = document.createElement('button');
                    slotButton.className = 'slot-button';
                    slotButton.innerHTML = `
                        <div class="slot-date">${slot.formatted_date}</div>
                        <div class="slot-time">${slot.formatted_time}</div>
                    `;

                    // Add click handler for the slot button
                    slotButton.addEventListener('click', () => {
                        const slotBookingForm = document.getElementById('slot-booking-form');
                        if (slotBookingForm) {
                            // Display the slot booking form
                            slotBookingForm.style.display = 'block';

                            // Pre-fill the date and time fields in the custom viewing form
                            const dateInput = document.getElementById('preferred_date');
                            const timeInput = document.getElementById('preferred_time');

                            if (dateInput) dateInput.value = slot.date;
                            if (timeInput) timeInput.value = slot.start_time;

                            // Attach the slot ID to the "Book Slot" button
                            const bookSlotButton = document.getElementById('book-slot-button');
                            if (bookSlotButton) {
                                bookSlotButton.setAttribute('data-slot-id', slot.id); // Dynamically set slot ID
                                bookSlotButton.onclick = () => requestSlotViewing(slot.id); // Ensure correct ID is passed
                            }
                        }
                    });

                    slotsWrapper.appendChild(slotButton);
                });

                slotsContainer.appendChild(slotsWrapper);
            } else {
                slotsContainer.innerHTML = '<p class="no-slots-message">No available slots at this time. Please use the custom viewing request form above.</p>';
            }
        } catch (error) {
            console.error('Error fetching slots:', error);
            const slotsContainer = document.getElementById('available-slots-container');
            if (slotsContainer) {
                slotsContainer.innerHTML = '<p class="error-message">Error loading available slots. Please try again later.</p>';
            }
        }
    }

    function requestSlotViewing(slotId) {
        // Validate slotId
        if (!slotId || slotId === 'undefined') {
            showModalMessage('Invalid slot selection. Please try again.');
            return;
        }
    
        const endpoint = `/real_estate/book_viewing_slot/${slotId}/`;
        
        // Get form data
        const name = document.getElementById('slot-name').value.trim();
        const contact = document.getElementById('slot-contact').value.trim();
        const email = document.getElementById('slot-email').value.trim();
        
        // Validate inputs
        if (!name || !contact || !email) {
            showModalMessage('All fields (Name, Contact, Email) are required.');
            return;
        }
        
        // Create request data
        const requestData = {
            name: name,
            contact: contact,
            email: email
        };
    
        // Make the API call
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Failed to book slot');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                showModalMessage('Viewing slot booked successfully!');
                // Close the booking form
                const slotBookingForm = document.getElementById('slot-booking-form');
                if (slotBookingForm) {
                    slotBookingForm.style.display = 'none';
                }
                // Optional: Reload after 2 seconds to show updated availability
                setTimeout(() => {
                    location.reload();
                }, 2000);
            } else {
                throw new Error(data.message || 'Failed to book slot');
            }
        })
        .catch(error => {
            console.error('Error booking slot:', error);
            showModalMessage(error.message || 'An error occurred while booking the slot.');
        });
    }
    
    // Event listener for slot selection
    document.addEventListener('DOMContentLoaded', function() {
        const slotsContainer = document.getElementById('available-slots-container');
        if (slotsContainer) {
            slotsContainer.addEventListener('click', function(e) {
                const slotButton = e.target.closest('.slot-button');
                if (slotButton) {
                    const slotId = slotButton.getAttribute('data-slot-id');
                    const slotBookingForm = document.getElementById('slot-booking-form');
                    if (slotBookingForm) {
                        slotBookingForm.style.display = 'block';
                        // Set the slot ID on the book button
                        const bookSlotButton = document.getElementById('book-slot-button');
                        if (bookSlotButton) {
                            bookSlotButton.setAttribute('data-slot-id', slotId);
                        }
                    }
                }
            });
        }
    
        // Event listener for booking button
        const bookSlotButton = document.getElementById('book-slot-button');
        if (bookSlotButton) {
            bookSlotButton.addEventListener('click', function() {
                const slotId = this.getAttribute('data-slot-id');
                requestSlotViewing(slotId);
            });
        }
    });

    // Function to handle viewing request submission
    async function submitViewingRequest(formType, slotId = null) {
        try {
            const formData = new FormData();
            const sourcePrefix = formType === 'slot' ? 'slot' : 'viewing';

            // Common fields for both forms
            const name = document.getElementById(`${sourcePrefix}-name`).value;
            const contact = document.getElementById(`${sourcePrefix}-contact`).value;
            const email = document.getElementById(`${sourcePrefix}-email`).value;

            formData.append('name', name);
            formData.append('contact', contact);
            formData.append('email', email);

            let url;
            if (formType === 'slot') {
                url = `/real_estate/book_viewing_slot/${slotId}/`;
            } else {
                // Additional fields for the custom viewing request
                const preferredDate = document.getElementById('preferred_date').value;
                const preferredTime = document.getElementById('preferred_time').value;
                const message = document.getElementById('viewing-message').value;

                formData.append('preferred_date', preferredDate);
                formData.append('preferred_time', preferredTime);
                formData.append('message', message);

                url = `/real_estate/request_custom_viewing/${document.getElementById('custom-viewing-form').dataset.propertyId}/`;
            }

            // Send the POST request
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
                showModalMessage(
                    formType === 'slot'
                        ? 'Viewing slot booked successfully!'
                        : 'Custom viewing request submitted successfully!'
                );
            } else {
                throw new Error('Server returned an error: ' + JSON.stringify(data.errors));
            }
        } catch (error) {
            showModalMessage('An error occurred. Please try again.');
            console.error(error);
        } finally {
            const modal = document.getElementById("viewingModal");
            if (modal) {
                modal.style.display = 'none';
            }
        }
    }

    // Event listener for custom viewing form submission
    document.getElementById('custom-viewing-form')?.addEventListener('submit', function (event) {
        event.preventDefault();
        submitViewingRequest('custom');
    });

    // Function to handle custom viewing requests
    function requestCustomViewing(propertyId) {
        const name = document.getElementById('viewing-name').value.trim();
        const contact = document.getElementById('viewing-contact').value.trim();
        const email = document.getElementById('viewing-email').value.trim();
        const date = document.getElementById('preferred_date').value;
        const time = document.getElementById('preferred_time').value;
        const message = document.getElementById('viewing-message').value.trim();

        // Validate required fields
        if (!name || !contact || !email || !date || !time) {
            showModalMessage('All fields are required.');
            return;
        }

        const endpoint = `/real_estate/request_custom_viewing/${propertyId}/`;
        const formData = new FormData();
        formData.append('name', name);
        formData.append('contact', contact);
        formData.append('email', email);
        formData.append('preferred_date', date);
        formData.append('preferred_time', time);
        formData.append('message', message);

        fetch(endpoint, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'An error occurred');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                showModalMessage('Custom viewing request submitted successfully!');
                // Close the viewing modal
                const viewingModal = document.getElementById('viewingModal');
                if (viewingModal) {
                    viewingModal.style.display = 'none';
                }
                // Optional: reload after 2 seconds
                setTimeout(() => {
                    location.reload();
                }, 2000);
            } else {
                showModalMessage(data.message || 'Failed to submit viewing request.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModalMessage(`An error occurred: ${error.message}`);
        });
    }

    // Event listener for custom viewing request
    const customViewingForm = document.getElementById('custom-viewing-form');
    if (customViewingForm) {
        customViewingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            clearModalMessages();  // Clear previous messages

            const contactInput = document.getElementById('viewing-contact');
            if (contactInput && !validateContactNumber(contactInput.value)) {
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

    // Function to display the "no slots available" message
    function displayNoSlotsMessage(container) {
        container.innerHTML = `
            <div class="alert alert-info" role="alert">
                <i class="fa-solid fa-info-circle" aria-hidden="true"></i>
                <p>No pre-scheduled viewing slots are currently available for this property.</p>
                <p>You can request a custom viewing time using the form above, and our team will contact you within 24 hours to arrange a suitable time.</p>
            </div>`;
    }

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
            const viewingModal = document.getElementById('viewingModal');

            if (viewingModal) {
                viewingModal.style.display = 'block';

                // Update the form's property ID
                const form = document.getElementById('custom-viewing-form');
                if (form) {
                    form.setAttribute('action', `/real_estate/request_custom_viewing/${propertyId}/`);
                    form.setAttribute('data-property-id', propertyId);
                }

                // Fetch and display available slots
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
                                slotButton.className = 'slot-button';
                                const date = new Date(slot.date);
                                const formattedDate = date.toLocaleDateString('en-GB', {
                                    weekday: 'long',
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric'
                                });
                                slotButton.innerHTML = `${formattedDate} ${slot.start_time} - ${slot.end_time}`;
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
                            displayNoSlotsMessage(slotsContainer);
                        }
                    })
                    .catch(error => {
                        const slotsContainer = document.getElementById('available-slots-container');
                        if (slotsContainer) {
                            displayNoSlotsMessage(slotsContainer);
                        }
                    });
            }
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

    // Update viewing button click handler
    document.querySelectorAll('.update-viewing-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const viewingId = this.getAttribute('data-viewing-id');
            const updateModal = document.getElementById('updateModal');
            const updateViewingForm = document.getElementById('updateViewingForm');
            
            try {
                // Fetch current viewing details and available slots
                const response = await fetch(`/real_estate/update_viewing/${viewingId}/`);
                const data = await response.json();
                
                // Populate form with current viewing details
                document.getElementById('viewingId').value = viewingId;
                document.getElementById('name').value = data.current_viewing.name;
                document.getElementById('contact').value = data.current_viewing.contact;
                document.getElementById('email').value = data.current_viewing.email;
                document.getElementById('message').value = data.current_viewing.message;
                document.getElementById('preferredDate').value = data.current_viewing.preferred_date;
                document.getElementById('preferredTime').value = data.current_viewing.preferred_time;

                // Display available slots
                const slotsContainer = document.getElementById('availableSlotsContainer');
                if (data.slots && data.slots.length > 0) {
                    const slotsHtml = data.slots.map(slot => `
                        <div class="available-slot">
                            Date: ${slot.date}<br>
                            Time: ${slot.start_time} - ${slot.end_time}
                        </div>
                    `).join('');
                    slotsContainer.innerHTML = slotsHtml;
                } else {
                    slotsContainer.innerHTML = '<p>No pre-defined slots available. Your request will require admin approval.</p>';
                }

                // Show the modal
                updateModal.style.display = 'block';
            } catch (error) {
                console.error('Error fetching viewing details:', error);
                showModalMessage('Error loading viewing details. Please try again.');
            }
        });
    });

    // Helper function to format time to HH:mm format
    function formatTimeForSubmission(timeValue) {
        try {
            // Check if time is already in correct format
            if (/^\d{2}:\d{2}$/.test(timeValue)) {
                return timeValue;
            }
            // Create a new date object with the time value
            const [hours, minutes] = timeValue.split(':');
            return `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
        } catch (error) {
            console.error('Error formatting time:', error);
            return timeValue; // Return original value if formatting fails
        }
    }

    // Form submission handler
    const updateViewingForm = document.getElementById('updateViewingForm');
    if (updateViewingForm) {
        updateViewingForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const viewingId = document.getElementById('viewingId').value;

            // Create FormData and ensure the time is in correct format
            const formData = new FormData(this);
            const timeValue = formData.get('preferred_time');

            // Format time to HH:mm format and validate
            if (timeValue) {
                try {
                    const [hours, minutes] = timeValue.split(':');
                    const formattedTime = `${hours.padStart(2, '0')}:${minutes.padStart(2, '0')}`;
                    formData.set('preferred_time', formattedTime);

                    // Log the formatted time for debugging
                    console.log('Formatted time:', formattedTime);
                } catch (error) {
                    console.error('Error formatting time:', error);
                    showModalMessage('Invalid time format. Please use HH:mm format.');
                    return;
                }
            }

            try {
                // Log the form data being sent
                console.log('Form data being sent:');
                for (let pair of formData.entries()) {
                    console.log(`${pair[0]}: ${pair[1]}`);
                }

                const response = await fetch(`/real_estate/update_viewing/${viewingId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    }
                });

                // Log the response for debugging
                console.log('Response status:', response.status);
                const data = await response.json();
                console.log('Response data:', data);

                if (data.status === 'success') {
                    showModalMessage(data.message);
                    setTimeout(() => {
                        location.reload();
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Unknown error occurred');
                }
            } catch (error) {
                console.error('Error updating viewing:', error);
                showModalMessage(`An error occurred: ${error.message}`);
            }
        });
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

    // Contact form handling
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(contactForm);
            fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCSRFToken()
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showModalMessage('Your message has been sent.');
                    contactForm.reset();
                } else {
                    showModalMessage('Failed to send your message. Please try again.');
                }
            })
            .catch(error => {
                showModalMessage('An error occurred: ' + error.message);
            });
        });
    }
});

// Function to show the modal with a message
function showModal(message) {
    const modal = document.getElementById('modal');
    const modalMessage = document.getElementById('modal-message');
    
    if (modal && modalMessage) {
        modalMessage.innerText = message;
        modal.style.display = 'block';
    } else {
        console.error("Modal or modal message element not found.");
    }
}

// Function to close the modal
function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.style.display = 'none';
    } else {
        console.error("Modal element not found.");
    }
}

// Function to move to the next step
function nextStep(step) {
    const currentInput = document.querySelector(`#step${step} input[type="number"]`);
    if (currentInput && !isValidInput(currentInput.value)) {
        showModal("Please enter a valid number greater than zero.");
        return;
    }
    document.getElementById(`step${step}`).classList.remove('active');
    document.getElementById(`step${step + 1}`).classList.add('active');
}

// Function to move to the previous step
function prevStep(step) {
    document.getElementById(`step${step}`).classList.remove('active');
    document.getElementById(`step${step - 1}`).classList.add('active');
}

// Function to validate input values
function isValidInput(value) {
    return value && value > 0;
}

// Function to calculate mortgage and display results
function calculateMortgage() {
    const propertyPrice = parseFloat(document.getElementById('propertyPrice').value);
    const deposit = parseFloat(document.getElementById('deposit').value);
    const term = parseInt(document.getElementById('term').value);
    const interestRate = parseFloat(document.getElementById('interestRate').value);

    if (!isValidInput(propertyPrice) || !isValidInput(deposit) || !isValidInput(interestRate)) {
        showModal("Please ensure all values are greater than zero.");
        return;
    }

    if (deposit >= propertyPrice) {
        showModal("Deposit cannot be greater than or equal to the property price.");
        return;
    }

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

// Function to update term value display
function updateTermValue(value) {
    document.getElementById('termValue').innerText = `${value} years`;
}

// Expose functions to global scope
window.nextStep = nextStep;
window.prevStep = prevStep;
window.updateTermValue = updateTermValue;
window.calculateMortgage = calculateMortgage;
window.showModal = showModal;
window.closeModal = closeModal;
