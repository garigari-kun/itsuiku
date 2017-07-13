from django.conf.urls import url

from .views import (
    UserSettingsView,
    DeleteUserAccount
)

urlpatterns = [
    url(r'^$', UserSettingsView.as_view(), name='main'),
    url(r'^delete$', DeleteUserAccount.as_view(), name='delete')
]
