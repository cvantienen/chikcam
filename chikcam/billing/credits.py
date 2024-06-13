from chikcam.users.models import User
from django.http import JsonResponse


def handle_purchase(customer_id, amount_paid):

    print('handling purchase')
    # Retrieve the user associated with this customer_id
    try:
        user = User.objects.get(stripe_customer_id=customer_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

    # Calculate credits based on the amount paid
    credits_bought = int(amount_paid)  # Assuming you want to add credits as whole numbers

    # Update the user's credits
    user.credits += credits_bought
    user.save()

    return JsonResponse({'status': 'success', 'credits_added': credits_bought}, status=200)
