from django.urls import path

from chikcam.billing.views import (
    billing_home,
    checkout,
    checkout_success,
)

app_name = "billing"
urlpatterns = [
    path("", view=billing_home, name="home"),
    path("checkout", view=checkout, name="checkout"),
    path("success", view=checkout_success, name="checkout_success"),

]
