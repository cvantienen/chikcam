from chikcam.users.models import User
import stripe


def handle_purchase(session):
    customer_id = session['customer']
    payment_intent_id = session['payment_intent']

    # Retrieve the payment intent to get the amount paid
    payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
    amount_paid = payment_intent['amount_received']  # Amount is in cents

    # Calculate credits based on the amount paid
    credits_bought = amount_paid / 100  # Assuming 1 credit per dollar

    # Retrieve the user associated with this customer_id
    user = User.objects.get(stripe_customer_id=customer_id)

    # Update the user's credits
    user.credits += credits_bought
    user.save()