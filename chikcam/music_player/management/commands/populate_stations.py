import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, APIC
from chikcam.music_player.models import Station, Track


class Command(BaseCommand):
    help = 'Populate the database with tracks from the media directory'

    def handle(self, *args, **kwargs):
        # Delete existing tracks and stations
        Track.objects.all().delete()
        Station.objects.all().delete()

        stations = [
            {'name': 'The Coop Hits', 'description': 'Chart-topping favorites clucked out loud from our nest to yours'},
            {'name': 'Rooster Rock Radio', 'description': 'Rocking the coop with classic and indie rock hits'},
            {'name': 'Eggstraordinary Beats', 'description': 'Cracking open the freshest beats from around the world'},
            {'name': 'Hen House Harmony', 'description': 'Where every song pecks at your emotions'},
            {'name': 'Cluckin Country', 'description': 'Your home for down-home tunes and feathered fun'},
        ]

        for station_data in stations:
            station, created = Station.objects.get_or_create(
                name=station_data['name'],
                defaults={'description': station_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created station: {station.name}'))

                # Add tracks to the station
                station_dir = os.path.join(settings.MEDIA_ROOT, 'tracks', station.name.lower().replace(' ', '_'))
                if os.path.exists(station_dir):
                    audio_files = sorted(os.listdir(station_dir))
                    for audio_file in audio_files:
                        audio_path = os.path.join(station_dir, audio_file)
                        # Assume the cover art filename matches the audio filename with .png extension
                        cover_art_filename = f"{os.path.splitext(audio_file)[0]}.png"
                        cover_art_path = os.path.join(settings.MEDIA_ROOT, 'cover_art', cover_art_filename)

                        # Extract metadata from the MP3 file
                        audio = MP3(audio_path, ID3=ID3)
                        title = audio.get('TIT2', TIT2(encoding=3, text=os.path.splitext(audio_file)[0])).text[0]
                        artist = audio.get('TPE1', TPE1(encoding=3, text='Unknown Artist')).text[0]
                        album = audio.get('TALB', TALB(encoding=3, text='Unknown Album')).text[0]

                        # Check if the cover art file exists
                        if os.path.exists(cover_art_path):
                            cover_art_rel_path = os.path.join('cover_art', cover_art_filename)
                        else:
                            print(f'file does not exist for cover art: {cover_art_path}')
                            cover_art_rel_path = None

                        with open(audio_path, 'rb') as f:
                            track_file = File(f)
                            new_track = Track.objects.create(
                                station=station,
                                title=title,
                                artist=artist,
                                album=album,
                                file=os.path.join('tracks', station.name.lower().replace(' ', '_'), audio_file),
                                cover_art=cover_art_rel_path
                            )
                            self.stdout.write(
                                self.style.SUCCESS(f'Added track: {audio_file} to station: {station.name}'))

                else:
                    self.stdout.write(self.style.WARNING(f'Track directory does not exist: {station_dir}'))
