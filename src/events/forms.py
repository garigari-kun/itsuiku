from django import forms

from .models import Event, Schedule


class EventModelForm(forms.ModelForm):

    title = forms.CharField(
        label="タイトル",
        required=True,
    )

    description = forms.CharField(
        label="メモ"
    )

    class Meta:
        model = Event
        fields = ['title', 'description']



class ScheduleModelForm(forms.ModelForm):

    date = forms.CharField(
        label='日付'
    )

    start_time = forms.CharField(
        label='開始時間',

    )

    end_time = forms.CharField(
        label='終了時間'
    )

    class Meta:
        model = Schedule
        fields = [
            'date',
            'start_time',
            'end_time'
        ]

# birth_date = forms.DateField(
#     label='生年月日',
#     required=False,
#     widget=SelectDateWidget(
#         attrs={'class': 'form-control'},
#         years=range(1900, now.year + 1),
#         months=MONTHS,
#     ),
# )
