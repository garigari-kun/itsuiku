from django.shortcuts import render
from django.views.generic.base import TemplateView, View


class TopView(View):

    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context(request)
        return render(request, self.template_name, context)

    def get_context(self, request, *args, **kwargs):
        context = {}
        return context
