from django.shortcuts import render

from django.views.generic.base import View




class ExpView(View):

    template_name = 'user_settings/done_deleting.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass
