from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('user-dashboard')
        template_name = 'accounts/login.html'
        context = {}
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        pass



class SignUpView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass




class LogOutView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
