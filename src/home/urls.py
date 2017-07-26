from django.conf.urls import url

from .views import (
    TopView,
    ContactFormView,
    ForumView
)

urlpatterns = [
    url(r'^$', TopView.as_view(), name='top'),
    url(r'^forum$', ForumView.as_view(), name='forum'),
    url(r'^contact$', ContactFormView.as_view(), name='contact'),
]
