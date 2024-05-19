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
    fetch(`/add-to-favorites/${propertyId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            alert('Property added to favorites!');
        } else {
            alert('Error adding property to favorites.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function scheduleViewing(propertyId) {
    fetch(`/schedule-viewing/${propertyId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'ok') {
            alert('Viewing scheduled successfully!');
        } else {
            alert('Error scheduling viewing.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function contactAgent(propertyId) {
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCSRFToken()
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'message sent') {
                    alert('Message sent to the agent!');
                } else {
                    alert('Error sending message.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Attach event listeners to action buttons if they exist
    document.querySelectorAll('.property-actions button').forEach(button => {
        button.addEventListener('click', function(event) {
            const propertyId = this.getAttribute('data-property-id');
            const action = this.getAttribute('data-action');

            if (action === 'addToFavorites') {
                addToFavorites(propertyId);
            } else if (action === 'scheduleViewing') {
                scheduleViewing(propertyId);
            } else if (action === 'contactAgent') {
                contactAgent(propertyId);
            }
        });
    });
});