from django.contrib import admin

from .models import Event, Schedule

@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'title',
        'created',
        'update'
    )



@admin.register(Schedule)
class ScheduleModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'date',
        'comment',
        # 'start_time',
        # 'end_time',
        'created',
    )
