from django.http import JsonResponse
from django.shortcuts import render
from .models import Station, Track


def music_player(request):
    stations = Station.objects.all()
    print(f'Music PLayer Html Request:{stations}')
    return render(request, 'music_player/music_player.html', {'stations': stations})


def stations_api(request):
    stations = Station.objects.all()
    data = []
    print(f'Music PLayer API Request:{stations}')
    for station in stations:
        tracks = [{
            'title': track.title,
            'artist': track.artist,
            'file_url': request.build_absolute_uri(track.file.url),
            'cover_art_url': request.build_absolute_uri(track.cover_art.url) if track.cover_art else '',
            'album': track.album,  # Ensure 'album' is included if it's part of the Track model
        } for track in station.track_set.all()]
        data.append({
            'id': station.id,
            'name': station.name,
            'tracks': tracks,
        })
    return JsonResponse(data, safe=False)
