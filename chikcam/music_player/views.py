from django.shortcuts import render
from django.http import JsonResponse
from .models import Station


def music_player(request):
    stations = Station.objects.all()
    return render(request, 'music_player/player.html', {'stations': stations})


def station_tracks(request, station_id):
    station = Station.objects.get(id=station_id)
    tracks = station.tracks.all()
    track_list = [{'title': track.title, 'file': track.file.url} for track in tracks]
    return JsonResponse({'tracks': track_list})
