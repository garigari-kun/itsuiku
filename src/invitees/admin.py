from django.contrib import admin

from .models import Attendance, Invitee


@admin.register(Attendance)
class AttendanceModelAdmin(admin.ModelAdmin):
    list_display  = (
        'pk',
        'choice'
    )


@admin.register(Invitee)
class InviteeModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'created',
        'updated'
    )
