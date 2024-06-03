from django.db import models


# Create your models here.
class Chicken(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),  # Optional, based on your need
    )
    BREED_CHOICES = (
        ('Silkie', 'Silkie'),
        ('Australorp', 'Australorp'),
        ('Sapphire Gem', 'Sapphire Gem'),
    )
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unknown')
    breed = models.CharField(max_length=200, choices=BREED_CHOICES, default='Unknown')
    image = models.ImageField(upload_to='chickens/images/')
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
