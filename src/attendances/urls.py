from django.conf.urls import url

from .views import EventTopView, CreateEventAttendanceView

urlpatterns = [
    url(r'^$', EventTopView.as_view(), name='top'),
    url(r'^create$', CreateEventAttendanceView.as_view(), name='create'),

]
