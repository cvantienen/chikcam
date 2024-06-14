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

// Function to display notifications
function displayNotification(message, type) {
  if (type === 'success') {
    // Display a success notification
    alert(`Success: ${message}`);
  } else if (type === 'error') {
    // Display an error notification
    alert(`Error: ${message}`);
  }
}
