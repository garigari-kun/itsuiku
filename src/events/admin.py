from django.contrib import admin

from .models import Event

@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'title',
        'created',
        'update'
    )
