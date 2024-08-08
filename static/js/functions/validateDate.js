const showModalMessage = require('./showModalMessage');
function validateDate() {
    const preferredDateInput = document.getElementById('preferred_date');
    const currentDate = new Date();
    const selectedDate = new Date(preferredDateInput.value);

    if (isNaN(selectedDate.getTime())) {
        showModalMessage('Please enter a valid date.');
        preferredDateInput.value = '';  // Clear invalid date
        return false;
    }

    if (selectedDate < currentDate.setHours(0, 0, 0, 0)) {
        showModalMessage('You cannot select a past date. Please choose a valid date.');
        preferredDateInput.value = '';  // Clear past date
        return false;
    }

    return true;
}

module.exports = validateDate;