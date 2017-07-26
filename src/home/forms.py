from django import forms



class ContactForm(forms.Form):

    CATEGORIES = [
        ('1', 'ご質問'),
        ('2', 'バグ報告'),
        ('3', '機能追加のリクエスト'),
        ('4', 'その他お問い合わせ')
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
        ),
        error_messages={
            'required': 'メールアドレスは必須です'
        }
    )

    url = forms.URLField(
        widget=forms.URLInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='URL',
        required=False,
    )

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        label='内容'
    )
