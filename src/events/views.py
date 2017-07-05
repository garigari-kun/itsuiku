from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import (
    EventModelForm,
    ScheduleModelForm,
    ScheduleDeletionCheckModelForm
)
from .models import Event, Schedule

from pprint import pprint




class DashboardView(LoginRequiredMixin, View):

    template_name = 'events/dashboard.html'
    login_url = '/account/login/'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    def get_context_data(self, request, *args, **kwargs):
        context = {}
        context['events'] = Event.objects.get_activeuser_events(request)
        return context


class CreateEventView(LoginRequiredMixin, View):


    login_url = '/account/login/'
    template_name = 'events/create_event.html'


    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)

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
            # form is invalid, rerender
            context = self.get_context_data(request)
            return render(request, self.template_name, context)

        return redirect('event:event-success', event_code=instance_of_event.event_code)



    def get_event_form(self, request, *args, **kwargs):
        form = EventModelForm(request.POST or None)
        return form

    def get_schedule_formset(self, request, extra=0, *args, **kwargs):
        ScheduleFormSet = formset_factory(ScheduleModelForm, extra=extra)
        formset = ScheduleFormSet(request.POST or None)
        return formset


    def get_context_data(self, request, *args, **kwargs):
        context = {}
        # form
        context['event_form'] = self.get_event_form(request)
        context['schedule_formset'] = self.get_schedule_formset(request, extra=0)

        return context



class EventCreationSuccessView(View):

    template_name = 'events/success.html'
    http_method_names = ['get']

    def get(self, request, event_code=None, *args, **kwargs):
        context = self.get_context_data(request, event_code=event_code)
        return render(request, self.template_name, context)

    def get_context_data(self, request, event_code=None, *args, **kwargs):
        context = {}
        context['event'] = get_object_or_404(Event, event_code=event_code)
        return context




class UpdateEventView(View):

    template_name = 'events/update_event.html'

    def get(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        event_form = self.get_event_form(request, instance=event)
        schedule_list = self.get_schedule_list(event)
        schedule_formset = self.get_schedule_formset(request, extra=0, postfix='schedule')
        schedule_deletion_formset = self.get_schedule_deletion_formset(
            request,
            instance=schedule_list,
            prefix='schedule_deletion'
        )
        context = {
            'event_form': event_form,
            'schedule_formset': schedule_formset,
            'schedule_list': schedule_list,
            'schedule_deletion_formset' : schedule_deletion_formset
        }
        return render(request, self.template_name, context)


    def post(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        event_form = self.get_event_form(request, instance=event)
        schedule_formset = self.get_schedule_formset(request, extra=0, postfix='schedule')
        schedule_list = self.get_schedule_list(event)
        schedule_deletion_formset = self.get_schedule_deletion_formset(request, prefix='schedule_deletion')

        if event_form.is_valid() and schedule_formset.is_valid() and schedule_deletion_formset.is_valid():
            # Updating Event model
            instance_of_event = event_form.save()

            print(schedule_formset)

            for schedule in schedule_formset:
                """
                Bug report:

                Even though, I post more than one schedule, it does not save except first one
                """
                # Inserting new Schedule records
                instance_of_schedule = schedule.save()
                instance_of_event.schedule_range.add(instance_of_schedule)

            for sd in schedule_deletion_formset:
                if sd.cleaned_data['deletion_check']:
                    print(sd.cleaned_data['id'])
                    # Delete schedule by looking up id
                    result = Schedule.objects.filter(id=sd.cleaned_data['id']).delete()

            return redirect('attendance:top', event_code=event.event_code)

        return HttpResponse('post has been sent')


    def get_event_form(self, request, instance=None, *args, **kwargs):
        form = EventModelForm(request.POST or None, instance=instance)
        return form

    def get_schedule_formset(self, request, extra=0, instance=None, prefix='', *args, **kwargs):
        ScheduleFormSet = formset_factory(ScheduleModelForm, extra=extra)
        formset = ScheduleFormSet(request.POST or None, initial=instance, prefix=prefix)
        return formset


    def get_schedule_deletion_formset(self, request, extra=0, instance=None, prefix='', *args, **kwargs):
        ScheduleDeletionCheckFormSet = formset_factory(ScheduleDeletionCheckModelForm, extra=extra)
        formset = ScheduleDeletionCheckFormSet(data=request.POST or None, initial=instance, prefix=prefix)
        return formset


    def get_schedule_list(self, event, *args, **kwargs):
        if event:
            schedule_list = []
            for schedule in event.schedule_range.all():
                tmp_dict = {
                    'id': schedule.id,
                    'date': schedule.date,
                    'comment': schedule.comment
                }
                schedule_list.append(tmp_dict)
        return schedule_list


    def get_context_data(self, request, *args, **kwargs):
        pass







class DeleteEventView(LoginRequiredMixin, View):
    def get(self, request, event_code=None, *args, **kwargs):
        return self.delete(request, event_code, *args, **kwargs)


    def post(self, request, event_code=None, *args, **kwargs):
        pass

    def delete(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        for schedule in event.schedule_range.all():
            schedule.delete()
            print(schedule)
        event.delete()
        return redirect('user-dashboard')
