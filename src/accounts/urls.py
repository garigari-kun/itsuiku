from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (
    LoginView,
    SignUpView,
    LogOutView,
    UserActivationView,
    SignUpSuccessView
)


urlpatterns = [
    url(r'^login/$',
        LoginView.as_view(),
        name='login'
    ),

    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup/success/$', SignUpSuccessView.as_view(), name='signup-success'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),

    url(r'^password_reset/$',
        auth_views.password_reset,
        {
            'template_name': 'accounts/login.html',
            'post_reset_redirect': 'account:password_reset_done'
        },
        name='password_reset'
    ),

    url(r'^password_reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'
    ),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'
    ),

    url(r'^reset/done/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'
    ),
    url(r'^account/user_activation/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        UserActivationView.as_view(),
        name='user_activation'
    ),

]
