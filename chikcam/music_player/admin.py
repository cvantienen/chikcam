from django.contrib import admin
from .models import Station, Track


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    inlines = [TrackInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('station', 'title', 'file', 'artist', 'album', 'cover_art')
    list_filter = ('station', 'artist', 'album')
    search_fields = ('title', 'artist', 'album')
