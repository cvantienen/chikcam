# Generated by Django 4.2.13 on 2024-06-03 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_customer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
