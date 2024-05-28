from django.db import models


class ActionButton(models.Model):
    ACTION_CHOICES = (
        ('feed_snack', 'Feed Snack'),
        ('flashlight', 'Flashlight'),
        ('text_to_talk', 'Text to Talk'),
        ('play_song', 'Play Song'),
        ('take_pic', 'Take a Pic'),
    )
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    activation_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.get_action_type_display()} - Activations: {self.activation_count}"

    def increment_activation(self):
        self.activation_count += 1
        self.save()
