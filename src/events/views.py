from django.shortcuts import render
from django.views.generic.base import TemplateView



class EventTopView(TemplateView):
    template_name = 'events/home.html'
