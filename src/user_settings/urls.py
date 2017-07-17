from django.conf.urls import url

from .views import (
    UserSettingsView,
    DeleteUserAccount,
    UserPasswordChangeView
)

urlpatterns = [
    url(r'^$', UserSettingsView.as_view(), name='main'),
    url(r'^change_password$', UserPasswordChangeView.as_view(), name='change_password'),
    url(r'^delete$', DeleteUserAccount.as_view(), name='delete')
]
