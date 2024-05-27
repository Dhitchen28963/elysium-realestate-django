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

function addToFavorites(propertyId) {
    console.log('Adding to favorites:', propertyId);
    fetch(`/add-to-favorites/${propertyId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
        if (data.status === 'ok') {
            alert('Property added to favorites!');
        } else if (data.status === 'exists') {
            alert('Property is already in favorites.');
        } else {
            alert('Error adding property to favorites.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function requestCustomViewing(propertyId) {
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
        console.log('Response from server:', data);
        if (data.status === 'ok') {
            alert('Viewing request sent to the agent!');
            // Hide the modal after a successful request
            const modal = document.getElementById("viewingModal");
            modal.style.display = "none";
        } else {
            alert('Error sending viewing request: ' + JSON.stringify(data.errors));
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function contactAgent(propertyId) {
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
        console.log('Response from server:', data);
        if (data.status === 'message sent') {
            alert('Message sent to the agent!');
        } else {
            alert('Error sending message.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Event listener for add to favorites
    document.querySelectorAll('.property-actions button[data-action]').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const propertyId = this.getAttribute('data-property-id');
            const action = this.getAttribute('data-action');

            if (action === 'addToFavorites') {
                addToFavorites(propertyId);
            }
        });
    });

    // Event listener for custom viewing request
    const customViewingForm = document.getElementById('custom-viewing-form');
    if (customViewingForm) {
        customViewingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const propertyId = customViewingForm.getAttribute('data-property-id');
            requestCustomViewing(propertyId);
        });
    }

    // Event listener for contact form submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const propertyId = contactForm.getAttribute('data-property-id');
            contactAgent(propertyId);
        });
    }

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
                console.log('Response from server:', data);
                if (data.status === 'ok') {
                    alert('Viewing request sent successfully.');
                    const modal = document.getElementById("viewingModal");
                    modal.style.display = "none";
                } else {
                    alert('Error sending viewing request: ' + JSON.stringify(data.errors));
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});
