// notification.js
$(document).ready(function() {
  // Define notification messages
  var messages = [
    "Notification 1",
    "Notification 2",
    "Notification 3"
  ];

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

  // Function to cycle through messages every 5 minutes
  function cycleMessages() {
    var index = 0;
    setInterval(function() {
      showToast(messages[index]);
      index = (index + 1) % messages.length;
    }, 300000); // 300000 milliseconds = 5 minutes
  }

  // Start cycling messages
  cycleMessages();
});
