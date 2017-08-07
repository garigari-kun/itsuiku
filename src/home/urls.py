from django.conf.urls import url

from .views import (
    ContactFormView,
    ForumView,
    TopView,
)

urlpatterns = [
    url(r'^$',
        TopView.as_view(),
        name='top'
    ),
    url(r'^contact$',
        ContactFormView.as_view(),
        name='contact'
    ),
    url(r'^forum$',
        ForumView.as_view(),
        name='forum'
    ),
]
