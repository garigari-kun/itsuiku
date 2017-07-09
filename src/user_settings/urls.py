from django.conf.urls import url

from .views import (
    UserSettingsView,
)

urlpatterns = [
    url(r'^$', UserSettingsView.as_view(), name='main')
]
