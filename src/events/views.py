from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import EventModelForm, ScheduleModelForm
from .models import Event, Schedule




class DashboardView(LoginRequiredMixin, View):

    template_name = 'events/dashboard.html'
    login_url = '/account/login/'

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(user=request.user, active=True)
        context = {
            'events': events,

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass



class CreateEventView(LoginRequiredMixin, View):


    login_url = '/account/login/'
    template_name = 'events/create_event.html'
    success_template_name = 'events/success.html'


    def get(self, request, *args, **kwargs):
        # form
        event_form = self.get_event_form(request)
        schedule_formset = self.get_schedule_formset(request, extra=0)
        # context
        context = {
            'event_form': event_form,
            'schedule_formset': schedule_formset
        }

        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):
        # form
        event_form = self.get_event_form(request)
        schedule_formset = self.get_schedule_formset(request, extra=0)

        if event_form.is_valid() and schedule_formset.is_valid():
            user = request.user
            instance_of_event = event_form.save(commit=False)
            instance_of_event.user = user
            instance_of_event.save()
            for schedule in schedule_formset:
                instance_of_schedule = schedule.save()
                instance_of_event.schedule_range.add(instance_of_schedule)
        else:
            context = {
                'event_form': event_form,
                'schedule_formset': schedule_formset
            }
            return render(request, self.template_name, context)

        context = {
            'event': instance_of_event
        }
        # WIP: After save, redirect to success view
        return redirect('event:event-success', event_code=instance_of_event.event_code)
        # return render(request, self.success_template_name, context)


    def get_event_form(self, request, *args, **kwargs):
        form = EventModelForm(request.POST or None)
        return form

    def get_schedule_formset(self, request, extra=0, *args, **kwargs):
        ScheduleFormSet = formset_factory(ScheduleModelForm, extra=extra)
        formset = ScheduleFormSet(request.POST or None)
        return formset



class EventCreationSuccessView(View):

    template_name = 'events/success.html'

    def get(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        context = {
            'event': event
        }
        return render(request, self.template_name, context)
