from .models import Event
from django.contrib.auth.models import User


user = User.objects.get(username='admin')

title = input('title: ')
description = input('desc: ')

event = Event(user=user, title=title, description=description)
event.save()
