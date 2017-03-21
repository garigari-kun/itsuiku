from django.conf.urls import url

from .views import (
    # EventTopView,
    DashboardView,
    CreateEventView
)


urlpatterns = [
    # url(r'^home/$', EventTopView.as_view(), name='home'),
    # url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^create/$', CreateEventView.as_view(), name='create-event'),
]
