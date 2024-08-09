const { editComment } = require('../../static/js/functions/editComment');

describe('editComment', () => {
    beforeEach(() => {
        document.body.innerHTML = `
            <div id="editModal" style="display: none;">
                <textarea id="editCommentBody"></textarea>
            </div>
            <button class="edit-comment" onclick="window.editComment(1, 'Test Comment')">Edit</button>
        `;
        window.editComment = editComment; // Attach to window object
    });

    test('should show modal with comment body on edit button click', () => {
        const editButton = document.querySelector('.edit-comment');
        editButton.click();

        const modal = document.getElementById('editModal');
        const textarea = document.getElementById('editCommentBody');

        expect(modal.style.display).toBe('block');
        expect(textarea.value).toBe('Test Comment');
    });
});
