from django.db import transaction
from django.http import JsonResponse
from django.conf import settings

import stripe

from .models import Payment
from chikcam.users.models import User


def credit_purchase(customer_id, amount_paid):
    print('Handling Credit purchase')
    # Convert amount_paid to the correct unit if necessary
    # Assuming amount_paid is in cents and 100 cents = 1 credit
    credits_bought = int(amount_paid)  # Convert from cents to credits
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


def record_purchase(customer_id, payment_intent):
    # Assuming you can get the user based on the customer_id
    user = User.objects.get(stripe_customer_id=customer_id)

    # Assuming payment_intent is an object with the necessary information
    Payment.objects.create(
        user=user,
        stripe_payment_intent_id=payment_intent.id,
        amount=payment_intent.amount / 100,  # Convert from cents to dollars
        currency=payment_intent.currency
    )


def use_credits(customer_id, credit_amount):
    print('Handling Credits Used')
    credits_used = int(credit_amount)  # Convert from cents to credits
    try:
        with transaction.atomic():
            user = User.objects.select_for_update().get(stripe_customer_id=customer_id)
            if user.credits < credits_used:
                return False  # Not enough credits
            user.credits -= credits_used
            user.save()
        return True  # Successfully used credits
    except User.DoesNotExist:
        raise ValueError('User not found')
    except Exception as e:
        print(f"Error using credits: {str(e)}")
        raise
