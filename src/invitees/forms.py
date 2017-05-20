from django import forms

from .models import Attendance, Invitee, ATTENDANCE_CHOICES


class InviteeModelForm(forms.ModelForm):
    class Meta:
        model = Invitee
        fields = [
            'name',
            'comment'
        ]


class AttendanceModelForm(forms.ModelForm):

    choice = forms.TypedChoiceField(
        choices=ATTENDANCE_CHOICES,
        widget=forms.RadioSelect,
        initial='yes'
    )

    class Meta:
        model = Attendance
        fields = [
            'choice'
        ]
