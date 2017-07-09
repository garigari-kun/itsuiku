from django.shortcuts import render
from django.views.generic.base import View



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
