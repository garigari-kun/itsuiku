from django.conf.urls import url

from .views import (
    EventTopView
)


urlpatterns = [
    url(r'^home/$', EventTopView.as_view(), name='home'),
]
