from chikcam.users.models import User
import stripe


def handle_purchase(customer_id, payment_intent):
    # Fulfill the purchase
    print('Connected account ID: ' + customer_id)
    print(str(payment_intent))

    # Retrieve the payment intent to get the amount paid
    amount_paid = payment_intent

    print(f'credits bought!: {payment_intent}')

    # Calculate credits based on the amount paid
    credits_bought = amount_paid

    # Retrieve the user associated with this customer_id
    user = User.objects.get(stripe_customer_id=customer_id)

    # Update the user's credits
    user.credits += credits_bought
    user.save()
