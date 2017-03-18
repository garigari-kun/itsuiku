from django import forms

from .models import Event, Schedule


class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
        'title',
        'description'
        ]


class ScheduleModelForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = [
            'date',
            'start_time',
            'end_time'
        ]
