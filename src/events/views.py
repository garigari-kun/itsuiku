from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.forms import formset_factory

from .forms import EventModelForm, ScheduleModelForm
from .models import Event, Schedule



class EventTopView(TemplateView):
    template_name = 'events/home.html'


class DashboardView(View):

    def get(self, request, *args, **kwargs):
        template_name = 'events/dashboard.html'
        context = {}
        return render(request, template_name, context)



class CreateEventView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'events/create_event.html'
        # form
        event_form = EventModelForm()

        ScheduleFormSet = formset_factory(ScheduleModelForm, extra=9)
        schedule_formset = ScheduleFormSet()

        context = {
            'event_form': event_form,
            'schedule_formset': schedule_formset
        }

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST or None)
        ScheduleFormSet = formset_factory(ScheduleModelForm, extra=9)
        schedule_formset = ScheduleFormSet(request.POST or None)
        if event_form.is_valid() and schedule_formset.is_valid():
            print('Eventform')
            print(repr(event_form))
            print('ScheduleFormSet')
            print(repr(ScheduleFormSet))
        else:
            print('Problem occured')
        return HttpResponse('OK')





class CreateEventViewWIP(CreateView):
    pass
    """
    Research
    1. Can I use two differenct ModelForm for this view?
    2. If so, can I name these differently and implement these separately???
    3. 1 can't be done, are there any good way of solving these? Just View is good choice?


    """
