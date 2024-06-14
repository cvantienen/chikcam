from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse, HttpRequest
from django.conf import settings
from django.views.decorators.csrf import requires_csrf_token

from .models import ActionButton
from chikcam.billing.credits import use_credits


def all_buttons_status(request: HttpRequest) -> JsonResponse:
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


@login_required()
@requires_csrf_token
def increment_button_activation(request, action_type):
    if request.method == 'POST':
        try:
            button = ActionButton.objects.get(action_type=action_type)
            cost = button.cost  # Assuming 'cost' is defined in your ActionButton model
            customer_id = request.user.stripe_customer_id
            if use_credits(customer_id, cost):
                button.increment_activation()
                # Include the button action_type in the success message
                return JsonResponse({"success": True, "message": f"Credits used to activate {button.action_type}."}, status=200)
            else:
                return JsonResponse({"success": False, "error": "Not enough credits"}, status=403)
        except ActionButton.DoesNotExist:
            return JsonResponse({"success": False, "error": "Button not found"}, status=404)
        except ValueError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": "Failed to use credits"}, status=500)
    else:
        return JsonResponse({"increment_button_activation error": "Method not allowed"}, status=405)
