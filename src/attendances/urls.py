from django.conf.urls import url

from .views import EventTopView

urlpatterns = [
    url(r'^$', EventTopView.as_view(), name='top'),

]
