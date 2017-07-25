from django.conf.urls import url

from .views import (
    TopView,
    ContactFormView
)

urlpatterns = [
    url(r'^$', TopView.as_view(), name='top'),
    url(r'^contact$', ContactFormView.as_view(), name='contact'),
]
