import { getCSRFToken } from './getCSRFToken.js';
import { showModalMessage } from './showModalMessage.js';
import { validateDate } from './validateDate.js';
import { clearModalMessages } from './clearModalMessages.js';

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

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
        })
        .then(response => response.json())
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
