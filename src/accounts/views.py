from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
)
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import (
    EmailUserForm,
    EmailUserLoginForm
)

from itsuiku.utils import send_confirmation_email
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('user-dashboard')

        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.get_user_login_form(request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                email=email,
                password=password
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'ようこそ！ログインしました')
                return redirect('user-dashboard')

        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        context['login_failed'] = '''ログインに失敗しました。\n
        ログインID、もしくはパスワードが間違っている可能性があります。
        '''
        return render(request, template_name, context)

    def get_user_login_form(self, request):
        form = EmailUserLoginForm(request.POST or None)
        return form

    def get_context_data(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.get_user_login_form(request)
        return context

    def get_template_name(self, request, *args, **kwargs):
        template_name = 'accounts/login.html'
        return template_name



class SignUpView(View):

    template_name = 'accounts/signup.html'


    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.get_user_form(request)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            new_user.is_active=False
            new_user.save()
            if new_user:
                result = send_confirmation_email(
                    request,
                    user=new_user,
                    subject_template='accounts/user_activation_subject.txt',
                    content_template='accounts/user_activation_email.html'
                )
                return render(request, self.get_template_name(request, type='post'), {})
                # return redirect('account:signup-success')
        else:
            context = self.get_context_data(request)
            return render(request, self.template_name, context)


    def get_user_form(self, request):
        form = EmailUserForm(request.POST or None)
        return form

    def get_template_name(self, request, type=None, *args, **kwargs):
        if type == 'post':
            template_name = 'accounts/signup_success.html'
        else:
            template_name = 'accounts/signup.html'
        return template_name

    def get_context_data(self, request, *args, **kwargs):
        context = {}
        context['form'] = self.get_user_form(request)
        return context



class UserActivationView(View):

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        klass = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = klass._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            template_name = self.get_template_name(request)
            context = self.get_context_data(request)
            return render(request, template_name, context)
        else:
            # message
            return redirect('home:top')


    def get_template_name(self, request):
        template_name = 'accounts/user_activation_success.html'
        return template_name

    def get_context_data(self, request):
        context = {}
        return context



class SignUpSuccessView(View):

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_name(request), self.get_context_data(request))


    def get_template_name(self, request, *args, **kwargs):
        template_name = 'accounts/signup_success.html'
        return template_name


    def get_context_data(self, request, *args, **kwargs):
        context = {}
        return context




class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:top')
