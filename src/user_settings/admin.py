from django.contrib import admin

from .models import UserProfile

@admin.register(UserProfile)
class UserSettingModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'username',
        'created',
        'updated'
    )
