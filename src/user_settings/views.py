from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View

from django.http import HttpResponse

from events.models import Event
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import UserPasswordChangeForm, UserProfileModelForm, PasswordResetRequestForm
from .models import UserProfile
from django.contrib.auth.tokens import default_token_generator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template import loader

from django.core.mail import send_mail





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
        return context

    def get_user_profile_form(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        print(user_profile)
        if user_profile:
            # Edit view
            form = UserProfileModelForm(request.POST or None, instance=user_profile)
        else:
            form = UserProfileModelForm(request.POST or None)
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
                s_info = {
                    'email': assoc_user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'itsuiku',
                    'uid': urlsafe_base64_encode(force_bytes(assoc_user.id)),
                    'user': assoc_user,
                    'token': default_token_generator.make_token(assoc_user),
                    'protocol': 'http'
                }
                print(repr(s_info))
                mail_subject_template_name = 'user_settings/password_reset_subject.txt'
                mail_content_template_name = 'user_settings/password_reset_email.html'
                subject = loader.render_to_string(mail_subject_template_name, s_info)
                content = loader.render_to_string(mail_content_template_name, s_info)
                print(subject)
                print(content)
                subject = ''.join(subject.splitlines())

                # send_mail(
                #     subject,
                #     content,
                #     DEFAULT_FROM_EMAIL ,
                #     [assoc_user.email],
                #     fail_silently=False
                # )

                """


# Email subject *must not* contain newlines
subject = ''.join(subject.splitlines())
email = loader.render_to_string(email_template_name, c)
send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
result = self.form_valid(form)
messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
return result
                """
            return HttpResponse('post valid')

        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)


    def get_template_name(self, request):
        template_name = 'user_settings/forgot_password.html'
        return template_name


    def get_context_data(self, request):
        context = {}
        context['p_r_form'] = self.get_password_reset_request_form(request)
        return context


    def get_password_reset_request_form(self, request):
        form = PasswordResetRequestForm(request.POST or None)
        return form
