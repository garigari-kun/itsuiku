from django.contrib import admin

from .models import UserSetting

@admin.register(UserSetting)
class UserSettingModelAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'user_fullname',
        'created',
        'updated'
    )
