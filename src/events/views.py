from django.shortcuts import render
from django.views.generic.base import TemplateView, View

from .forms import EventModelForm, ScheduleModelForm
from .models import Event, Schedule



class EventTopView(TemplateView):
    template_name = 'events/home.html'



class CreateEventView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'events/create_event.html'
        # form
        event_form = EventModelForm()
        schedule_form = ScheduleModelForm()

        context = {
            'event_form': event_form,
            'schedule_form': schedule_form,
        }

        return render(request, template_name, context)
