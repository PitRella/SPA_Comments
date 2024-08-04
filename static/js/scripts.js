// Ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const previewButton = document.getElementById('preview-button'); // The button to preview the comment
    const commentForm = document.getElementById('comment-form'); // The form containing the comment
    const previewSection = document.getElementById('preview-section'); // The section where the preview will be shown

    // Add a click event listener to the preview button
    previewButton.addEventListener('click', function() {
        // Create a FormData object from the comment form
        const formData = new FormData(commentForm);

        // Send a POST request to the server to preview the comment
        fetch('{% url "preview_comment" %}', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Include CSRF token in the request headers
            }
        })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
            // Update the preview section with the server's response
            previewSection.innerHTML = data.preview;
        })
        .catch(error => console.error('Error:', error)); // Log any errors to the console
    });
});

// Function to toggle the display of the reply form
function toggleReplyForm(commentId) {
    // Get the reply form element for the given comment ID
    const form = document.getElementById(`reply-form-${commentId}`);

    // Toggle the display style between 'none' and 'block'
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// Function to sort the table based on the clicked header
function sortTable(th) {
    // Get the sorting criteria from the header's attributes
    const sortBy = th.getAttribute('data-sort-by');
    let currentOrder = th.getAttribute('data-current-order');

    // Toggle the sorting order between 'asc' and 'desc'
    currentOrder = currentOrder === 'asc' ? 'desc' : 'asc';

    // Create a URL object from the current page URL
    const url = new URL(window.location.href);

    // Update the URL parameters for sorting
    url.searchParams.set('sort_by', sortBy);
    url.searchParams.set('order', currentOrder);

    // Redirect to the updated URL to sort the table
    window.location.href = url.toString();
}

// Function to add a tag to the textarea at the current cursor position
function addTag(tag) {
    // Get the textarea element by its ID
    const textarea = document.getElementById('id_text');

    // Get the current cursor position
    const startPos = textarea.selectionStart;
    const endPos = textarea.selectionEnd;

    // Get the current value of the textarea
    const text = textarea.value;

    // Split the text into before and after the cursor
    const before = text.substring(0, startPos);
    const after = text.substring(endPos, text.length);

    // Insert the tag at the cursor position
    textarea.value = `${before}${tag}${after}`;

    // Set the cursor position after the tag
    textarea.setSelectionRange(startPos + tag.length / 2, startPos + tag.length / 2);

    // Focus on the textarea
    textarea.focus();
}
