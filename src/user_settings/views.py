from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View

from django.http import HttpResponse

from events.models import Event
from django.contrib.auth import get_user_model
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

    # def get_user_password_change_form(self, request, *args, **kwargs):
    #     form = UserPasswordChangeForm(request.POST or None, request.user)
    #     return form




class DeleteUserAccount(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(user=request.user)
        for event in events:
            event.delete_event_and_relations()
        # Delete the user model
        deleting_user = get_object_or_404(get_user_model(), id=request.user.id)
        deleting_user.delete()
        return redirect('home:top')
