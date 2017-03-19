from django.shortcuts import render
from django.views.generic.base import TemplateView


class TopView(TemplateView):
    template_name = 'home/index.html'