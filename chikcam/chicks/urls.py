from django.urls import path

from chikcam.chicks.views import (
    chicks_stream,
)

app_name = "chicks"
urlpatterns = [
    path("", view=chicks_stream, name="home"),
]
