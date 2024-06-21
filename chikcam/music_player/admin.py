from django.contrib import admin
from .models import Station, Track


# Register your models here.
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


# Register your models here.
@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('station', 'title', 'file')

