async function addToFavorites(propertyId, app, showModalMessage) {
    try {
        const response = await fetch(`/api/add-to-favorites/${propertyId}/${app}/`);
        const data = await response.json();

        if (data.status === 'ok') {
            showModalMessage('Property added to favorites!');
            return data;
        } else if (data.status === 'exists') {
            showModalMessage('Property is already in favorites.');
            return data;
        } else {
            throw new Error('Error adding property to favorites');
        }
    } catch (error) {
        console.error('Error:', error);
        showModalMessage('An error occurred. Please try again.');
        throw error;
    }
}

module.exports = addToFavorites;