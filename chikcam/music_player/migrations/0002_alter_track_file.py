# Generated by Django 4.2.13 on 2024-06-21 21:00

import chikcam.music_player.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_player', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='file',
            field=models.FileField(upload_to=chikcam.music_player.models.track_upload_to),
        ),
    ]