const getCSRFToken = require('./getCSRFToken');
const showModalMessage = require('./showModalMessage');
const { validateDate } = require('./validateDate');

async function requestCustomViewing(propertyId) {
    const customViewingForm = document.getElementById('custom-viewing-form');
    const formData = new FormData(customViewingForm);

    if (!validateDate()) {
        return; // Exit early if date is invalid
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
            return data;
        } else {
            throw new Error('Server returned an error: ' + JSON.stringify(data.errors));
        }
    } catch (error) {
        console.error('Error:', error);
        showModalMessage('An error occurred while sending the viewing request. Please try again.');
        throw error;
    } finally {
        const modal = document.getElementById("viewingModal");
        modal.style.display = "none";
    }
}

module.exports = requestCustomViewing;