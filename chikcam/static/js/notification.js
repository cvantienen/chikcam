// Adjusted function to get CSRF token from meta tag
function getCSRFToken() {
  return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

// Updated AJAX setup to use the new function
function activateButton(actionType) {
  $.ajax({
    type: 'POST',
    url: `/esp32/increment/${actionType}/`, // Adjust the URL as needed
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
    },
    success: function(response) {
      // On success, display a success notification to the user
      displayNotification(response.message, 'success');
    },
    error: function(xhr) {
      // On error, parse the JSON response and display an error notification
      const response = JSON.parse(xhr.responseText);
      displayNotification(response.error, 'error');
    }
  });
}

// Function to display a message
function displayNotification(message, tags) {
    const messagesContainer = document.getElementById('messages');
    if (!messagesContainer) {
        console.error('Messages container not found');
        return;
    }
    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${tags} alert-dismissible justify-content-center text-center mb-3`;
    messageDiv.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;
    messagesContainer.appendChild(messageDiv);

    // Automatically remove the message after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Automatically remove messages after 5 seconds on page load
window.addEventListener('DOMContentLoaded', () => {
  const messagesContainer = document.getElementById('messages');
  if (messagesContainer) {
    const messages = messagesContainer.querySelectorAll('.alert');
    messages.forEach((message, index) => {
      setTimeout(() => {
        message.remove();
      }, 5000); // Adjust the timeout duration as needed
    });
  }
});
