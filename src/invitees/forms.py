from django import forms

from .models import Attendance, Invitee


class InviteeModelForm(forms.ModelForm):
    class Meta:
        model = Invitee
        fields = [
            'name',
            'comment'
        ]


class AttendanceModelForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'choice'
        ]
