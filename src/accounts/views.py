from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, View

from .forms import EmailUserForm


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
        template_name = 'accounts/signup.html'
        form = EmailUserForm()
        context = {
            'form': form,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        pass




class LogOutView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass




# def register(request):
#     template_name = 'registration/register.html'
#     if request.method == 'POST':
#         is_success, context = register_post(request)
#         if is_success:
#             return redirect('dashboard:dashboard')
#     else:
#         form = EmailUserForm()
#         context = {
#             'form': form,
#         }
#     return render(request, template_name, context)
#
#
# def register_post(request):
#     form = EmailUserForm(request.POST)
#     is_success = False
#     context = {}
#     if form.is_valid():
#         new_user = form.save(commit=False)
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password1']
#         new_user.save()
#         login_user = authenticate(email=email, password=password)
#         if login_user is not None:
#             if login_user.is_active:
#                 login(request, login_user)
#                 is_success = True
#                 return is_success, context
#     else:
#         context = {
#             'form': form,
#         }
#     return is_success, context
