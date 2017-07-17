"""itsuiku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin



from events.views import DashboardView

urlpatterns = [
    url(r'^', include('home.urls', namespace='home')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('accounts.urls', namespace='account')),
    url(r'^dashboard/$', DashboardView.as_view(), name='user-dashboard'),
    url(r'^event/', include('events.urls', namespace='event')),
    url(r'^user_settings/', include('user_settings.urls', namespace='user-settings')),
    url(r'^(?P<event_code>[\w-]+)/', include('attendances.urls', namespace='attendance')),
]
