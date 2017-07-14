from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View

from django.http import HttpResponse

from events.models import Event
from django.contrib.auth import get_user_model



class UserSettingsView(View):

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        pass

    def get_template_name(self, request, *args, **kwargs):
        template_name = 'user_settings/user_settings.html'
        return template_name

    def get_context_data(self, request, *args, **kwargs):
        context = {}
        return context




class DeleteUserAccount(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(user=request.user)
        for event in events:
            event.delete_event_and_relations()
        # Delete the user model
        deleting_user = get_object_or_404(get_user_model(), id=request.user.id)
        deleting_user.delete()
        return redirect('home:top')
