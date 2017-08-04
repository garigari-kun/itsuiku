from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View

from django.http import HttpResponse

from events.models import Event
from django.contrib.auth import get_user_model, update_session_auth_hash, logout
from .forms import (
    UserPasswordChangeForm,
    UserProfileModelForm,
    PasswordResetRequestForm,
    ChangeUserEmailForm
)
from .models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template import loader

from django.core.mail import send_mail

from itsuiku.utils import send_confirmation_email





class UserSettingsView(View):

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        user_profile_form = self.get_user_profile_form(request)
        if user_profile_form.is_valid():
            i_user_profile_form = user_profile_form.save(commit=False)
            i_user_profile_form.user = request.user
            i_user_profile_form.save()
            return redirect('user-settings:main')

    def get_template_name(self, request, *args, **kwargs):
        template_name = 'user_settings/user_settings.html'
        return template_name

    def get_context_data(self, request, *args, **kwargs):
        context = {}
        # context['u_p_c_form'] = self.get_user_password_change_form(request)
        context['user_profile_form'] = self.get_user_profile_form(request)
        context['change_user_email_form'] = self.get_change_user_email_form(request)
        return context

    def get_user_profile_form(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except:
            form = UserProfileModelForm(request.POST or None)
            return form

        form = UserProfileModelForm(request.POST or None, instance=user_profile)
        return form


    def get_change_user_email_form(self, request, *args, **kwargs):
        form = ChangeUserEmailForm(request.POST or None)
        return form




class UserPasswordChangeView(View):

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def post(self, request, *args, **kwargs):
        u_p_c_form = self.get_user_password_change_form(request)
        if u_p_c_form.is_valid():
            user = u_p_c_form.save()
            update_session_auth_hash(request, user)
            return redirect('user-settings:main')
        return HttpResponse('error processing needed')


    def get_context_data(self, request, *args, **kwargs):
        context = {}
        context['u_p_c_form'] = self.get_user_password_change_form(request)
        return context


    def get_template_name(self, request, *args, **kwargs):
        template_name = 'user_settings/change_password.html'
        return template_name


    def get_user_password_change_form(self, request, *args, **kwargs):
        form = UserPasswordChangeForm(request.user, request.POST or None)
        return form




class DeleteUserAccount(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(user=request.user)
        for event in events:
            event.delete_event_and_relations()
        # Delete the user model
        deleting_user = get_object_or_404(get_user_model(), id=request.user.id)
        deleting_user.delete()
        return redirect('home:top')



class PasswordResetRequestView(View):

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def post(self, request, *args, **kwargs):
        form = self.get_password_reset_request_form(request)
        if form.is_valid():
            email = form.cleaned_data['email']
            assoc_user = get_user_model().objects.get(email=email)
            if assoc_user:
                result = send_confirmation_email(request,
                    user=assoc_user,
                    subject_template='user_settings/password_reset_subject.txt',
                    content_template='user_settings/password_reset_email.html'
                )
                print(result)
            return render(request, self.get_template_name(request, 'form_valid'), {})

        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def get_template_name(self, request, tmp_switch=None):
        template_name = 'user_settings/forgot_password.html'
        if tmp_switch == 'form_valid':
            template_name = 'user_settings/password_reset_notification.html'
        return template_name


    def get_context_data(self, request):
        context = {}
        context['p_r_form'] = self.get_password_reset_request_form(request)
        return context


    def get_password_reset_request_form(self, request):
        form = PasswordResetRequestForm(request.POST or None)
        return form


class PasswordResetConfirmationView(View):

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def post(self, request, uidb64=None, token=None, *args, **kwargs):
        form = self.get_password_change_form(request)
        if form.is_valid():
            klass = get_user_model()
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = klass._default_manager.get(pk=uid)
            except (TypeError, ValueError, OverflowError, klass.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                new_password= form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return redirect('user-settings:reset_password_success')
            else:
                # message
                return redirect('home:top')
        else:
            template_name = self.get_template_name(request)
            context = self.get_context_data(request)
            return render(request, template_name, context)



    def get_template_name(self, request):
        template_name = 'user_settings/reset_password.html'
        return template_name


    def get_context_data(self, request):
        context = {}
        context['p_c_form'] = self.get_password_change_form(request)
        return context


    def get_password_change_form(self, request):
        form = UserPasswordChangeForm(request.user, request.POST or None)
        return form


class PasswordResetSuccessView(View):

    def get(self, request, uidb64=None, token=None, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def get_template_name(self, request):
        template_name = 'user_settings/reset_password_success.html'
        return template_name


    def get_context_data(self, request):
        context = {}
        return context




class ChangeUserEmailView(View):

    def post(self, request, *args, **kwargs):
        form = self.get_change_user_email_form(request)
        if form.is_valid():
            new_useremail = form.cleaned_data['username']
            user = get_user_model().objects.get(email=request.user.email)
            user.email = new_useremail
            user.is_active = False
            user.save()
            if user:
                result = send_confirmation_email(
                    request,
                    user=user,
                    subject_template='accounts/user_activation_subject.txt',
                    content_template='accounts/user_activation_email.html'
                )
                logout(request)
                return redirect('home:top')
        else:
            # message sent
            return redirect('user-settings:main')


    def get_change_user_email_form(self, request):
        form = ChangeUserEmailForm(request.POST or None)
        return form



class ConfirmChangingUserEmailView(View):

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
        template_name = 'user_settings/confirm_changing_useremail.html'
        return template_name

    def get_context_data(self, request):
        context = {}
        return context










#
