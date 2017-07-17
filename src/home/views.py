from django.shortcuts import render
from django.views.generic.base import View


class TopView(View):


    def get(self, request, *args, **kwargs):
        context = self.get_context(request)
        template_name = self.get_template_name(request)
        return render(request, template_name, context)

    def get_context(self, request, *args, **kwargs):
        context = {}
        return context

    def get_template_name(self, request, *args, **kwargs):
        template_name = 'home/index.html'
        return template_name
