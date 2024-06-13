# Generated by Django 4.2.13 on 2024-06-13 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esp32', '0002_remove_actionbutton_last_activated'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionbutton',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='actionbutton',
            name='last_activated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
