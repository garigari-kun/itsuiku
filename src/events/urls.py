from django.conf.urls import url

from .views import (
    CreateEventView
)


urlpatterns = [
    # url(r'^home/$', EventTopView.as_view(), name='home'),
    # url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^create/$', CreateEventView.as_view(), name='create-event'),
    # url(r'^(?P<event_code>[\w-]+)/$', EventTopView.as_view(), name='EventTopView'),
]



#     url(r'^(?P<shortcode>[\w-]+)/$', URLRedirectView.as_view(), name='shortcode_redirect'),
