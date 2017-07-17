from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View

from django.http import HttpResponse

from events.models import Event
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import UserPasswordChangeForm, UserProfileModelForm
from .models import UserProfile



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
        print(request.user)
        return render(request, template_name, context)


    def post(self, request, *args, **kwargs):
        u_p_c_form = self.get_user_password_change_form(request)
        if u_p_c_form.is_valid():
            user = u_p_c_form.save()
            update_session_auth_hash(request, user)  # Important!
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
