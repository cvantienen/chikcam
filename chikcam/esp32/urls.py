from django.urls import path
from .views import increment_button_activation, all_buttons_status

from django.conf import settings


app_name = "esp32"
urlpatterns = [
    # Ensure this pattern is defined to catch the '/test/' endpoint
    path('status/', all_buttons_status, name='all_buttons_status'),
    path('<str:action_type>/', increment_button_activation, name='increment_action'),
]
