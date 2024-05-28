from django.urls import path
from .views import increment_button_activation

app_name = "esp32"
urlpatterns = [
    path('<str:action_type>/', increment_button_activation, name='increment_action'),
]
