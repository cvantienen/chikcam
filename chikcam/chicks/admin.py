from django.contrib import admin
from .models import Chicken


# Register your models here.
@admin.register(Chicken)
class ChickenAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'breed', 'image', 'description', 'created_at', 'updated_at')
