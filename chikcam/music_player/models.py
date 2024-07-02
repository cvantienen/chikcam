# music_player/models.py

from django.db import models
import os


def track_upload_to(instance, filename):
    print(filename)
    station_name = instance.station.name.lower().replace(' ', '_')
    return os.path.join('tracks', station_name, filename)


def cover_art_upload_to(filename):
    filename, extension = os.path.splitext(filename)
    return os.path.join('cover_art', f"{filename}.png")


class Station(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Track(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, null=True, blank=True)
    album = models.CharField(max_length=200, null=True, blank=True)
    file = models.FileField(upload_to=track_upload_to)
    cover_art = models.ImageField(upload_to=cover_art_upload_to, null=True, blank=True)

    def __str__(self):
        return self.title


class VoiceRecord(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='voice_recordings/')
    stations = models.ManyToManyField('Station', related_name='voice_recordings')

    def __str__(self):
        return self.title
