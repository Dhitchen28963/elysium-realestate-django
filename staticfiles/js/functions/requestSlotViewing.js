async function requestSlotViewing(viewingId) {
    try {
        const response = await fetch(`/real_estate/book_viewing_slot/${viewingId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        const data = await response.json();
        if (data.status === 'ok') {
            document.getElementById('viewingModal').style.display = 'block';
        } else {
            document.getElementById('viewingModal').style.display = 'none';
        }
    } catch (error) {
        document.getElementById('viewingModal').style.display = 'none';
        throw new Error('Network response was not ok');
    }
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

module.exports = {
    requestSlotViewing
};
