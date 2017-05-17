from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin


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




class DashboardView(LoginRequiredMixin, View):

    template_name = 'events/dashboard.html'
    login_url = '/account/login/'



    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)



class CreateEventView(LoginRequiredMixin, View):


    login_url = '/account/login/'
    template_name = 'events/create_event.html'


    def get(self, request, *args, **kwargs):
        # form
        event_form = EventModelForm()

        ScheduleFormSet = modelformset_factory(Schedule, form=ScheduleModelForm)
        schedule_formset = ScheduleFormSet()

        context = {
            'event_form': event_form,
            'schedule_formset': schedule_formset
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        event_form = EventModelForm(request.POST or None)
        ScheduleFormSet = modelformset_factory(Schedule, form=ScheduleModelForm)
        schedule_formset = ScheduleFormSet(request.POST or None)
        if event_form.is_valid() and schedule_formset.is_valid():
        # if event_form.is_valid():
            print('valid')
            user = request.user
            instance_of_event = event_form.save(commit=False)
            instance_of_event.user = user
            #instance_of_event.save()
            for schedule in schedule_formset:
                print(schedule)
                #instance_of_schedule = schedule.save()
                #instance_of_event.schedule_range.add(instance_of_schedule)
        else:
            print('Not valid')
            context = {
                'event_form': event_form,
                'schedule_formset': schedule_formset
            }
            return render(request, self.template_name, context)

        template_name = 'events/success.html'
        context = {
            'event': instance_of_event
        }
        return render(request, template_name, context)
