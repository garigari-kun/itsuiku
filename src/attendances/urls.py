from django.conf.urls import url

from .views import EventTopView, CreateEventAttendanceView, UpdateEventAttendanceView

urlpatterns = [
    url(r'^$', EventTopView.as_view(), name='top'),
    url(r'^create$', CreateEventAttendanceView.as_view(), name='create'),
    url(r'^(?P<invitee_id>\d+)/update$', UpdateEventAttendanceView.as_view(), name='update'),

]
