# Generated by Django 4.2.13 on 2024-07-02 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_player', '0004_alter_track_cover_art'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='voice_recordings/')),
                ('stations', models.ManyToManyField(related_name='voice_recordings', to='music_player.station')),
            ],
        ),
    ]
