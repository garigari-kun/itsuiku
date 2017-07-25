from django import forms



class ContactForm(forms.Form):

    CATEGORIES = [
        ('1', '質問')
    ]


    category = forms.ChoiceField(
        choices=CATEGORIES,
        label='お問い合わせカテゴリ',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(
            attrs={
                'class' : 'form-control'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        label='内容'
    )
    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='URL'
    )
