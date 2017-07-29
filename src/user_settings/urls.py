from django.conf.urls import url

from .views import (
    UserSettingsView,
    DeleteUserAccount,
    UserPasswordChangeView,
    PasswordResetRequestView,
    PasswordResetConfirmationView,
    PasswordResetSuccessView,
    ChangeUserEmailView
)

urlpatterns = [
    url(r'^$',
        UserSettingsView.as_view(),
        name='main'
    ),
    url(r'^change_password$',
        UserPasswordChangeView.as_view(),
        name='change_password'
    ),
    url(r'^delete$',
        DeleteUserAccount.as_view(),
        name='delete'
    ),
    url(r'^reset_password$',
        PasswordResetRequestView.as_view(),
        name='reset_password'
    ),
    url(r'^reset_password/success$',
        PasswordResetSuccessView.as_view(),
        name='reset_password_success'
    ),
    url(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmationView.as_view(),
        name='reset_password_confirm'
    ),
    url(r'^change_user_email$',
        ChangeUserEmailView.as_view(),
        name='change_user_email'
    ),

]
