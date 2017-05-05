from django.shortcuts import render
from django.views.generic.base import TemplateView, View


# class TopView(TemplateView):
#     template_name = 'home/index.html'


class TopView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'home/index.html'
        context = {}
        return render(request, template_name, context)
