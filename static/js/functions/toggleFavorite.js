const { getCSRFToken } = require('./getCSRFToken');
const { showModalMessage } = require('./showModalMessage');

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
        throw error;
    }
}

module.exports = { toggleFavorite };