from django.conf.urls import url

from .views import (
    CreateEventView,
    DeleteEventView,
    EventCreationSuccessView,
    UpdateEventView
)


urlpatterns = [
    url(r'^create/$',
        CreateEventView.as_view(),
        name='create-event'),
    url(r'^(?P<event_code>[\w-]+)/success/$',
        EventCreationSuccessView.as_view(),
        name='event-success'),
    url(r'^(?P<event_code>[\w-]+)/delete/$',
        DeleteEventView.as_view(),
        name='delete-event'),
    url(r'^(?P<event_code>[\w-]+)/update/$',
        UpdateEventView.as_view(),
        name='update-event')

]



#     url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='shortcode_redirect'),
