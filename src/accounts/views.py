from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.shortcuts import render, redirect
from django.views.generic.base import View

from .forms import EmailUserForm, EmailUserLoginForm


class LoginView(View):

    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('event:create-event')

        form = self.get_form(request)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.get_form(request)
        context = {}
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                email=email,
                password=password
            )
            if user is not None:
                login(request, user)
                return redirect('event:create-event')

        context['login_failed'] = '''ログインに失敗しました。\n
        ログインID、もしくはパスワードが間違っている可能性があります。
        '''
        context['form'] = form
        return render(request, self.template_name, context)


    def get_form(self, request):
        form = EmailUserLoginForm(request.POST or None)
        return form


class SignUpView(View):

    template_name = 'accounts/signup.html'


    def get(self, request, *args, **kwargs):
        form = self.get_form(request)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.get_form(request)
        if form.is_valid():
            new_user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            new_user.save()
            login_user = authenticate(email=email, password=password)
            if login_user is not None:
                if login_user.is_active:
                    login(request, login_user)
                    return redirect('event:create-event')
        else:
            context = {
                'form': form,
            }
            return render(request, self.template_name, context)


    def get_form(self, request):
        form = EmailUserForm(request.POST or None)
        return form



class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:top')
