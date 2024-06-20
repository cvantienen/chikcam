# music_player/urls.py
from django.urls import path
from.views import music_player, station_tracks

app_name = "music_player"
urlpatterns = [
    path('', music_player, name=''),
    path('station/<int:station_id>/tracks/', station_tracks, name='station_tracks'),
]
