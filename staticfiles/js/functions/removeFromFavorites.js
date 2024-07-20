const getCSRFToken = require('./getCSRFToken');
const showModalMessage = require('./showModalMessage');

async function removeFromFavorites(propertyId, app) {
    try {
        const response = await fetch(`/${app}/remove-from-favorites/${propertyId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({})
        });

        const data = await response.json();

        if (data.status === 'ok') {
            showModalMessage('Property removed from favorites!');
            location.reload();
            return data; // Ensure data is returned
        } else {
            showModalMessage('Error removing property from favorites.');
            throw new Error('Error removing property from favorites.');
        }
    } catch (error) {
        console.error('Error:', error);
        showModalMessage('An error occurred. Please try again.');
        throw new Error('An error occurred');
    }
}

module.exports = removeFromFavorites;