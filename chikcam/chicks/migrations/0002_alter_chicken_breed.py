# Generated by Django 4.2.13 on 2024-06-03 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chicks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chicken',
            name='breed',
            field=models.CharField(choices=[('Silkie', 'Silkie'), ('Australorp', 'Australorp'), ('Sapphire Gem', 'Sapphire Gem')], default='Unknown', max_length=200),
        ),
    ]
