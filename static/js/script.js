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
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('contact-form').addEventListener('submit', function(event) {
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
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});