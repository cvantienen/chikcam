from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings

from .models import ActionButton


def all_buttons_status(request):
    if request.method == 'GET':
        # Retrieve the token from the request headers
        request_token = request.headers.get('Authorization')

        # Check if the token is correct
        if request_token != settings.ESP32_API_TOKEN:
            return JsonResponse({"ESP32_API_TOKEN error": "Unauthorized"}, status=401)

        buttons = ActionButton.objects.all()
        data = {
            "buttons": [
                {"action_type": button.action_type, "activation_count": button.activation_count}
                for button in buttons
            ]
        }
        return JsonResponse(data, safe=False)
    else:
        # Corrected the error message to reflect the actual unsupported method
        return JsonResponse({"all_buttons_status error": "Method not allowed"}, status=405)


# Removed @login_required decorator
def increment_button_activation(request, action_type):
    if request.method == 'POST':
        # Retrieve the token from the request headers
        request_token = request.headers.get('Authorization')

        # Check if the token is correct
        if request_token != settings.ESP32_API_TOKEN:
            return JsonResponse({"ESP32_API_TOKEN error": "Unauthorized"}, status=401)

        try:
            button = ActionButton.objects.get(action_type=action_type)
            button.increment_activation()
            # Assuming 'chicks:home' is a placeholder, you might want to return a JsonResponse instead
            return JsonResponse({"success": True, "message": "Button activation incremented"}, status=200)
        except ActionButton.DoesNotExist:
            return JsonResponse({"success": False, "error": "Button not found"}, status=404)
    else:
        return JsonResponse({"increment_button_activation error": "Method not allowed"}, status=405)
