from django.contrib import admin
from .models import ActionButton


# Register your models here.
@admin.register(ActionButton)
class ActionButtonAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'activation_count')
