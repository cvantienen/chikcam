// notification.js
$(document).ready(function() {
  // Define a single notification message
  var message = "Notification 1";

  // Function to display toast with message
  function showToast(message) {
    var toastHtml = `
      <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-autohide="true">
        <div class="toast-header">
          <strong class="mr-auto">Notification</strong>
          <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="toast-body">
          ${message}
        </div>
      </div>
    `;

    $('.toast-container').append(toastHtml);
    $('.toast').toast('show');
  }

  // Show the message after 3 seconds
  setTimeout(function() {
    showToast(message);
  }, 3000); // 3000 milliseconds = 3 seconds
});
