from django.db import transaction
from django.http import JsonResponse
from django.conf import settings
import stripe
from chikcam.users.models import User


def handle_purchase(customer_id, amount_paid):
    print('Handling purchase')
    # Convert amount_paid to the correct unit if necessary
    # Assuming amount_paid is in cents and 100 cents = 1 credit
    credits_bought = int(amount_paid / 100)  # Convert from cents to credits

    try:
        with transaction.atomic():
            # Retrieve the user associated with this customer_id
            user = User.objects.select_for_update().get(stripe_customer_id=customer_id)

            # Update the user's credits
            user.credits += credits_bought
            user.save()

        return JsonResponse({'status': 'success', 'credits_added': credits_bought}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
    except Exception as e:
        # Log the error for debugging
        print(f"Error adding credits: {str(e)}")
        return JsonResponse({'status': 'error', 'message': 'Failed to add credits'}, status=500)



def handle_button_press(request, button_type):
    # Check if the request is POST
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    user = request.user
    button_costs = {
        'button1': 100,
        'button2': 50,
        # Add more buttons and their costs here
    }

    cost = button_costs.get(button_type)

    if cost is None:
        return JsonResponse({'status': 'error', 'message': 'Invalid button type'}, status=400)

    if user.credits < cost:
        return JsonResponse({'status': 'error', 'message': 'Insufficient credits'}, status=403)

    # Deduct credits
    user.credits -= cost
    user.save()

    # Perform the action associated with the button here
    # For example, turning on a light, playing a sound, etc.

    return JsonResponse({'status': 'success', 'message': f'{button_type} activated', 'remaining_credits': user.credits},
                        status=200)
