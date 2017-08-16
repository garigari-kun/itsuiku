from django import forms

from .models import Attendance, Invitee, ATTENDANCE_CHOICES


class InviteeModelForm(forms.ModelForm):

    name = forms.CharField(
        label='お名前',
        required=True,
        max_length=12,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    comment = forms.CharField(
        label='一言メモ',
        required=False,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


    class Meta:
        model = Invitee
        fields = [
            'name',
            'comment'
        ]


class AttendanceModelForm(forms.ModelForm):

    # choice = forms.TypedChoiceField(
    #     choices=ATTENDANCE_CHOICES,
    #     widget=forms.RadioSelect,
    #     initial='yes'
    # )

    choice = forms.TypedChoiceField(
        choices=ATTENDANCE_CHOICES,
        widget=forms.RadioSelect,
        label=''
    )


    class Meta:
        model = Attendance
        fields = [
            'choice',

        ]
