from django.conf.urls import url

from .views import (
    TopView,
)

urlpatterns = [
    url(r'^$', TopView.as_view(), name='top')
]
