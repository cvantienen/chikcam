# music_player/management/commands/populate_stations.py
import os
from django.core.management.base import BaseCommand
from chikcam.music_player.models import Station, Track


class Command(BaseCommand):
    help = 'Populate the database with predefined stations and tracks'

    def handle(self, *args, **kwargs):
        # Delete existing stations and tracks
        Track.objects.all().delete()
        Station.objects.all().delete()

        stations = [
            {'name': 'Rooster Rock Radio', 'description': 'Rocking the coop with classic and indie rock hits'},
            {'name': 'Eggstraordinary Beats', 'description': 'Cracking open the freshest beats from around the world'},
            {'name': 'The Coop Hits', 'description': 'Chart-topping favorites clucked out loud from our nest to yours'},
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
                station_dir = os.path.join('media', 'tracks', station.name.lower().replace(' ', '_'))
                if os.path.exists(station_dir):
                    audio_files = sorted(os.listdir(station_dir))
                    for audio_file in audio_files:
                        audio_path = os.path.join(station_dir, audio_file)
                        Track.objects.create(
                            station=station,
                            title=os.path.splitext(audio_file)[0],
                            file=audio_path
                        )
                        self.stdout.write(self.style.SUCCESS(f'Added track: {audio_file} to station: {station.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Track directory does not exist: {station_dir}'))
