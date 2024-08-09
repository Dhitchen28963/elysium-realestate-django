function editComment(commentId, commentBody) {
    const modal = document.getElementById('editModal');
    const textarea = document.getElementById('editCommentBody');

    modal.style.display = 'block';
    textarea.value = commentBody;
}

module.exports = {
    editComment
};
