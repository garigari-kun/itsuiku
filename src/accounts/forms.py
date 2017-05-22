from django import forms
from django.contrib.auth import get_user_model

class EmailUserForm(forms.ModelForm):

    """ A form for creating new user.

    """
    error_messages = {
        'duplicated_email': 'このメールアドレスは既に使用されています。',
        'password_mismatch': '入力されたパスワードが一致しませんでした。'
    }

    email = forms.CharField(
        label='メールアドレス',
        error_messages = {
            'required': 'メールアドレスは必須です',
            'invalid': 'このメールアドレスは不正です',
        },
    )

    password1 = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput,
        error_messages = {
            'required': 'パスワードは必須です',
        },
    )

    password2 = forms.CharField(
        label='確認パスワード',
        widget=forms.PasswordInput,
        error_messages = {
            'required': 'パスワードは必須です',
        },
        # help_text='確認のため、同じパスワードを入力して下さい'
    )

    class Meta:
        model = get_user_model()
        fields = [
            'email',
        ]

    def clean_email(self):
        """ Clean for email

        :return str email: Cleaned email address
        :raise forms.ValidationError: このメールアドレスは既に使用されています。

        """
        email = self.cleaned_data['email']
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicated_email'],
            code='duplicate_email',
        )

    def clean_password2(self):
        """ Check that the two passwords are matched.

        :return str password2: Cleaned password2
        :raise forms.ValidationError: password2 != password1

        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        """ Save user.

        Save the provided password in hashed format.

        :return custom_user.models.EmailUser: user

        """

        user = super(EmailUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class EmailUserLoginForm(forms.Form):

    email = forms.CharField(
        label='メールアドレス',
        error_messages={
            'required': 'メールアドレスが入力されていません',
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': 'パスワードが入力されていません',
        }
    )
