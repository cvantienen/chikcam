# music_player/models.py
from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Track(models.Model):
    station = models.ForeignKey(Station, related_name='tracks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='tracks/')

    def __str__(self):
        return self.title
