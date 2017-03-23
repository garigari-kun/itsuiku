from django.conf import settings
from django.db import models

from .utils import code_generator, create_event_code


class Schedule(models.Model):
    date = models.DateField(null=True, blank=True)
    # start_time = models.TimeField(null=True, blank=True)
    # end_time = models.TimeField(null=True, blank=True)
    comment = models.CharField(max_length=120, null=True, blank=True)
    # is_allday = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return '{}: {} {}'.format(self.pk, self.date, self.start_time)


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    event_code = models.CharField(max_length=12, unique=True)
    active = models.BooleanField(default=True)
    # schedule = models.ManyToManyField(Schedule, null=True, blank=True)
    schedule = models.ManyToManyField(Schedule, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        if self.event_code is None or self.event_code == '':
            self.event_code = create_event_code(self)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.title)
