# Generated by Django 4.2.13 on 2024-05-28 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esp32', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionbutton',
            name='last_activated',
        ),
    ]
