from django.shortcuts import render

from django.views.generic.base import View

from events.models import Event, Schedule
from events.forms import EventModelForm, ScheduleModelForm, ScheduleDeletionCheckMOdelForm



class FormExpView(View):

    template_name = ''


    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
