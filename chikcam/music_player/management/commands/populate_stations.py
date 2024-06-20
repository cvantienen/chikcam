# music_player/management/commands/populate_stations.py
import os
from django.core.management.base import BaseCommand
from chikcam.music_player.models import Station, Track
import random


class Command(BaseCommand):
    help = 'Populate the database with predefined stations and tracks'

    def handle(self, *args, **kwargs):
        stations = [
            {'name': 'Rock Station', 'description': 'The best rock music'},
            {'name': 'Jazz Station', 'description': 'Smooth jazz tunes'},
            {'name': 'Pop Station', 'description': 'Top pop hits'},
        ]

        for station_data in stations:
            station, created = Station.objects.get_or_create(
                name=station_data['name'],
                defaults={'description': station_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created station: {station.name}'))

                # Add tracks to the station
                music_dir = os.path.join('media', 'tracks', station.name.lower().replace(' ', '_'), 'music')
                voice_dir = os.path.join('media', 'tracks', station.name.lower().replace(' ', '_'), 'voice')

                if os.path.exists(music_dir) and os.path.exists(voice_dir):
                    music_files = os.listdir(music_dir)
                    voice_files = os.listdir(voice_dir)
                    combined_files = list(zip(music_files, voice_files))
                    random.shuffle(combined_files)

                    for music_file, voice_file in combined_files:
                        music_path = os.path.join(music_dir, music_file)
                        voice_path = os.path.join(voice_dir, voice_file)

                        Track.objects.create(
                            station=station,
                            title=os.path.splitext(music_file)[0],
                            file=music_path
                        )
                        self.stdout.write(self.style.SUCCESS(f'Added music track: {music_file} to station: {station.name}'))

                        Track.objects.create(
                            station=station,
                            title=os.path.splitext(voice_file)[0],
                            file=voice_path
                        )
                        self.stdout.write(self.style.SUCCESS(f'Added voice track: {voice_file} to station: {station.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Track directories do not exist: {music_dir} or {voice_dir}'))
