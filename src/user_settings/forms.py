from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile



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
        self.user.set_password(password)
        if commit:
            self.user.save()

        return self.user





class UserProfileModelForm(forms.ModelForm):

    username = forms.CharField(
        max_length=24,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='ユーザー名',
        error_messages={
            'required': '入力が必須です'
        },
        help_text='イベント登録時、タイトルに表示される名前です'
    )


    class Meta:
        model = UserProfile
        fields = [
            'username'
        ]





class PasswordResetRequestForm(forms.Form):

    email = forms.CharField(
        label='メールアドレス',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        error_messages={
            'required': '入力が必須です'
        }
    )


    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_user_model().objects.filter(email=email)
        if user:
            return email
        else:
            raise forms.ValidationError(
                'ユーザーは存在しません'
            )




class ChangeUserEmailForm(forms.Form):


    error_messages = {
        'duplicated_email': 'このメールアドレスは既に使用されています。',
        'username_mismatch': '入力されたメールアドレスが一致しませんでした。',
    }


    username = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='新しいメールアドレス',
        error_messages={
            'required': '入力が必須です'
        }
    )

    confirmed_username = forms.EmailField(
        max_length=128,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='確認用メールアドレス',
        error_messages={
            'required': '入力が必須です'
        }
    )


    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            get_user_model()._default_manager.get(email=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicated_email'],
            code='duplicated_email',
        )




    def clean_confirmed_username(self):
        # username = self.cleaned_data['username']
        username = self.data.get('username')
        username2 = self.cleaned_data['confirmed_username']

        if username and username2 and username != username2:
            raise forms.ValidationError(
                self.error_messages['username_mismatch'],
                code='username_mismatch'
            )

        return username2











#
