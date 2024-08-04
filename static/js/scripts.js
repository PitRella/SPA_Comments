document.addEventListener('DOMContentLoaded', function() {
    const previewButton = document.getElementById('preview-button');
    const commentForm = document.getElementById('comment-form');
    const previewSection = document.getElementById('preview-section');

    previewButton.addEventListener('click', function() {
        const formData = new FormData(commentForm);
        fetch('{% url "preview_comment" %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            previewSection.innerHTML = data.preview;
        })
        .catch(error => console.error('Error:', error));
    });
});

function toggleReplyForm(commentId) {
    const form = document.getElementById(`reply-form-${commentId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

function sortTable(th) {
    const sortBy = th.getAttribute('data-sort-by');
    let currentOrder = th.getAttribute('data-current-order');
    currentOrder = currentOrder === 'asc' ? 'desc' : 'asc';
    const url = new URL(window.location.href);
    url.searchParams.set('sort_by', sortBy);
    url.searchParams.set('order', currentOrder);
    window.location.href = url.toString();
}

function addTag(tag) {
    const textarea = document.getElementById('id_text');
    const startPos = textarea.selectionStart;
    const endPos = textarea.selectionEnd;
    const text = textarea.value;
    const before = text.substring(0, startPos);
    const after = text.substring(endPos, text.length);
    textarea.value = `${before}${tag}${after}`;
    textarea.setSelectionRange(startPos + tag.length / 2, startPos + tag.length / 2);
    textarea.focus();
}
