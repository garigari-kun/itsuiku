from django.conf.urls import url

from .views import LoginView, SignUpView, LogOutView


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
]
