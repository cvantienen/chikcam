from django.urls import path
from django.conf import settings

from chikcam.billing.views import (
    checkout,
    checkout_success,
    stripe_webhook,
    checkout_2,
)

app_name = "billing"
urlpatterns = [
    path("checkout", view=checkout, name="checkout"),
    path("checkout_2", view=checkout_2, name="checkout_2"),
    path("success", view=checkout_success, name="checkout_success"),
    path(settings.STRIPE_WEB_HOOK, stripe_webhook, name='stripe-webhook'),
]
