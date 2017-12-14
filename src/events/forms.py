from django import forms

from .models import Event, Schedule


class EventModelForm(forms.ModelForm):

    title = forms.CharField(
        label="タイトル",
        required=False,
        max_length=24,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    description = forms.CharField(
        label="メモ",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Event
        fields = ['title', 'description']


    def clean_title(self):
        title = self.cleaned_data['title']
        if not title:
            raise forms.ValidationError(
                'タイトルは必須項目です'
            )
        return title



class ScheduleModelForm(forms.ModelForm):

    date = forms.DateField(
        label='',
        widget=forms.DateInput(attrs={
            'placeholder': '日付',
            'class': 'form-control s-date-input',
            'readonly': 'readonly',
            'style': 'max-width: 100px;'
        })
    )

    comment = forms.CharField(
        max_length=24,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': '時間、一言メモ',
            'class': 'form-control s-comment-input time-picker'
        })
    )

    class Meta:
        model = Schedule
        fields = [
            'date',
            'comment',
        ]


class ScheduleDeletionCheckModelForm(forms.ModelForm):

    id = forms.CharField(
        widget=forms.HiddenInput()
    )

    # deletion_check = forms.CharField(
    #     widget=forms.CheckboxInput(),
    #     label=''
    # )
    deletion_check = forms.BooleanField(
        label='',
        required=False,
    )


    class Meta:
        model = Schedule
        fields = [
            'id'
        ]
