# music_player/urls.py
from django.urls import path
from .views import music_player, stations_api

app_name = "music_player"
urlpatterns = [
    path('', music_player, name='music_player'),
    path('api/stations/', stations_api, name='stations_api')
]
