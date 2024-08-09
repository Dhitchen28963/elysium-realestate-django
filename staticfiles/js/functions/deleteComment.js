import { getCSRFToken } from './getCSRFToken.js';
import { showModalMessage } from './showModalMessage.js';

// Delete comment handling
document.querySelectorAll('button.delete-comment').forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault();

        const commentId = this.getAttribute('data-id');
        const deleteModal = document.getElementById('deleteModal');

        if (!deleteModal) {
            showModalMessage('Delete comment modal not found.');
            return;
        }

        deleteModal.style.display = 'block';

        const confirmDeleteButton = document.getElementById('confirmDelete');
        if (!confirmDeleteButton) {
            showModalMessage('Confirm delete button not found.');
            return;
        }

        confirmDeleteButton.onclick = function () {
            const urlPrefix = window.location.pathname.includes('faq') ? '/faq' : '/blog';

            fetch(`${urlPrefix}/comment/${commentId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`comment-${commentId}`).remove();
                    deleteModal.style.display = 'none';
                    showModalMessage('Comment deleted successfully.');
                } else {
                    showModalMessage('An error occurred: ' + data.error);
                }
            })
            .catch(error => {
                showModalMessage('An error occurred.');
            });
        };
    });
});
