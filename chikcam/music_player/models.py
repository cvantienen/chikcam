# music_player/models.py
from django.db import models
import os


def track_upload_to(instance, filename):
    # Generate the upload path based on the station name
    station_name = instance.station.name.lower().replace(' ', '_')
    return os.path.join('tracks', station_name, filename)


class Station(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Track(models.Model):
    station = models.ForeignKey(Station, related_name='tracks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=track_upload_to)

    def __str__(self):
        return self.title
