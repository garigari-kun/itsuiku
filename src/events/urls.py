from django.conf.urls import url

from .views import (
    CreateEventView,
    EventCreationSuccessView
)


urlpatterns = [
    url(r'^create/$', CreateEventView.as_view(), name='create-event'),
    url(r'^(?P<event_code>[\w-]+)/success/$', EventCreationSuccessView.as_view(), name='event-success')
]



#     url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='shortcode_redirect'),
