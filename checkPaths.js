const path = require('path');

const filesToCheck = [
    './static/js/functions/addToFavorites',
    './static/js/functions/getCSRFToken',
    './static/js/functions/showModalMessage',
    './static/js/functions/setupEventListeners',
    './static/js/functions/mortgageCalculation',
    './static/js/functions/removeFromFavorites',
    './static/js/functions/clearModalMessages',
    './static/js/functions/validateDate'
];

filesToCheck.forEach(file => {
    try {
        require(path.resolve(__dirname, file));
        console.log(`Successfully required ${file}`);
    } catch (error) {
        console.error(`Failed to require ${file}:`, error.message);
    }
});
