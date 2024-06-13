// Function to call the increment_button_activation endpoint
function activateButton(actionType) {
  $.ajax({
    type: 'POST',
    url: `/esp32/increment/${actionType}/`, // Adjust the URL as needed
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    },
    success: function(response) {
      // On success, display a success notification to the user
      displayNotification(response.message, 'success');
    },
    error: function(xhr, status, error) {
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
    alert(`Success: ${message}`); // This can be replaced with a more sophisticated notification mechanism
  } else if (type === 'error') {
    // Display an error notification
    alert(`Error: ${message}`); // This can be replaced with a more sophisticated notification mechanism
  }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


