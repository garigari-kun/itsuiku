from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.forms import formset_factory

from .forms import EventModelForm, ScheduleModelForm
from .models import Event, Schedule



class EventTopView(View):
    # test event code : dcmqrez5b591
    def get(self, request, event_code=None, *args, **kwargs):
        template_name = 'events/event-top.html'
        event = get_object_or_404(Event, event_code=event_code)
        context = {
            'event': event,

        }
        print(event_code)
        return render(request, template_name, context)




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
            """
            print('Eventform')
            print(repr(event_form))
            print('ScheduleFormSet')
            print(repr(ScheduleFormSet))
            """
            user = request.user
            instance_of_event = event_form.save(commit=False)
            instance_of_event.user = user
            instance_of_event.save()
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
