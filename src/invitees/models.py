from django.db import models

from events.models import Event, Schedule



ATTENDANCE_CHOICES = (
    ('yes', 'yes'),
    ('mmm', 'mmm'),
    ('no', 'no')
)


class Attendance(models.Model):
    event = models.ForeignKey(Event)
    schedule = models.ForeignKey(Schedule)
    choice = models.CharField(max_length=4, choices=ATTENDANCE_CHOICES)

    def __str__(self):
        return '{}: {}'.format(self.id, self.choice)




class Invitee(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=120)
    attendance = models.ManyToManyField(Attendance)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ''.format(self.name)
