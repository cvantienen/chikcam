from chikcam.users.models import User
import math


def handle_purchase(customer_id, payment_intent):
    # Fulfill the purchase
    print('Connected account ID: ' + customer_id)
    print(str(payment_intent))

    # Retrieve the payment intent to get the amount paid
    amount_paid = payment_intent['amount']

    print(f'Amount paid: {amount_paid}')

    credits_bought = round(amount_paid)  # Round to the nearest whole number

    # Retrieve the user associated with this customer_id
    user = User.objects.get(stripe_customer_id=customer_id)

    # Update the user's credits
    user.credits += credits_bought
    user.save()
