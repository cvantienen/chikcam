

from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


class ActionButtonTests(TestCase):
    def test_all_buttons_status_with_authorization(self):
        # Set up the client
        client = Client()

        # Define the correct token
        correct_token = settings.ESP32_API_TOKEN

        # Get the URL for the view (replace 'all_buttons_status' with the actual name if it's different)
        url = reverse('esp32:all_buttons_status')  # Or use a direct path string if not named

        # Make the GET request with the Authorization header
        response = client.get(url, HTTP_AUTHORIZATION=correct_token)

        # Assert the response status code (200 OK expected if the token is correct)
        self.assertEqual(response.status_code, 200)

        # Additional assertions can be made here to check the response content
