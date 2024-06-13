from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .credits import handle_purchase
import stripe

# Create your views here.
@login_required
def billing_home(request: HttpRequest):
    return render(request, "billing/billing_home.html")


@login_required
def checkout(request: HttpRequest):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_TEST_KEY
        if request.user.stripe_customer_id:
            customer_id = request.user.stripe_customer_id
        else:
            customer = stripe.Customer.create(
                email=request.user.email
            )
            customer_id = customer['id']
            request.user.stripe_customer_id = customer_id
            request.user.save()
        session = stripe.checkout.Session.create(
            customer=customer_id,
            line_items=[
                {
                    # Credits
                    'price': 'price_1PP7hlECrDARISveU39gU1x1',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('chicks:stream')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('chicks:home')),
        )
        return redirect(session.url, code=303)
    return render(request, "billing/checkout.html")


@login_required
def checkout_2(request: HttpRequest):
    if request.method == "POST":
        stripe.api_key = settings.STRIPE_TEST_KEY
        if request.user.stripe_customer_id:
            customer_id = request.user.stripe_customer_id
        else:
            customer = stripe.Customer.create(
                email=request.user.email
            )
            customer_id = customer['id']
            request.user.stripe_customer_id = customer_id
            request.user.save()
        session = stripe.checkout.Session.create(
            customer=customer_id,
            line_items=[
                {
                    # raffle
                    'price': 'price_1PQCvCECrDARISveg6YFGR2w',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('billing:checkout_success')) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('chicks:home')),
        )
        return redirect(session.url, code=303)
    return render(request, "billing/checkout.html")


@login_required
def checkout_success(request: HttpRequest):
    session_id = request.GET['session_id']
    stripe.api_key = settings.STRIPE_TEST_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    print(session)
    return render(request, "chicks/stream.html")


@csrf_exempt
def stripe_webhook(request: HttpRequest):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SIGNATURE
        )
    except ValueError as e:
        # Invalid payload
        return JsonResponse({'status': 'invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({'status': 'invalid signature'}, status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        connected_account_id = payment_intent.get('account')  # Adjust this line
        handle_purchase(connected_account_id, payment_intent)

    return JsonResponse({'status': 'success'}, status=200)
