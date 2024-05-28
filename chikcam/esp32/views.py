from django.shortcuts import redirect

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ActionButton


@require_POST
def increment_button_activation(request, action_type):
    try:
        button = ActionButton.objects.get(action_type=action_type)
        button.increment_activation()
        return redirect('chicks:home')
    except ActionButton.DoesNotExist:
        return JsonResponse({"success": False, "error": "Button not found"}, status=404)
