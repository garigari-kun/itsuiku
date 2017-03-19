from django.conf.urls import url

from .views import (
    EventTopView,
    CreateEventView
)


urlpatterns = [
    url(r'^home/$', EventTopView.as_view(), name='home'),
    url(r'^event/create/$', CreateEventView.as_view(), name='create-event'),
]
