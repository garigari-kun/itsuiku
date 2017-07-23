from django.conf.urls import url

from .views import (
    EventTopView,
    CreateEventAttendanceView,
    UpdateEventAttendanceView,
    DeleteEventAttendanceView
)

urlpatterns = [
    url(r'^$', EventTopView.as_view(), name='top'),
    url(r'^create_schedule$', CreateEventAttendanceView.as_view(), name='create'),
    url(r'^(?P<invitee_id>\d+)/update_schedule$', UpdateEventAttendanceView.as_view(), name='update'),
    url(r'^(?P<invitee_id>\d+)/delete_schedule$', DeleteEventAttendanceView.as_view(), name='delete'),
]
