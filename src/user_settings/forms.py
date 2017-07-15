from django import forms


class UserPasswordChangeForm(forms.Form):


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    error_messages = {
        'password_mismatch': '入力されたパスワードが一致しませんでした。'
    }

    password1 = forms.CharField(
        label='新しいパスワード',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': 'パスワードは必須です'
        }
    )

    password2 = forms.CharField(
        label='新しいパスワード(確認)',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': '確認用パスワードは必須です'
        },
        help_text='確認のため、同じパスワードを入力して下さい'
    )

    def clean_password2(self):
        """ Check whether two passwords are same

        :return str password2: Cleaned password2
        :raise forms.ValidationError: password2 != password1
        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch'
            )

        return password2


    def save(self, commit=True):
        password = self.cleaned_data['password1']
        print(password)




















#
