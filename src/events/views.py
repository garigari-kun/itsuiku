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

        return redirect('event:event-success', event_code=instance_of_event.event_code)



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


class UpdateEventView(View):

    template_name = 'events/update_event.html'

    def get(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        event_form = self.get_event_form(request, instance=event)
        schedule_list = self.get_schedule_list(event)
        # schedule_formset should be new registration
        schedule_formset = self.get_schedule_formset(request, extra=0)

        # Deletion form test
        schedule_deletion_formset = self.get_scheduledeletion_formset(request, instance=schedule_list)


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
        schedule_formset = self.get_schedule_formset(request, extra=0)
        # scheudle_deletion_formset
        schedule_list = self.get_schedule_list(event)
        schedule_deletion_formset = self.get_scheduledeletion_formset(request, instance=schedule_list)


        if event_form.is_valid() and schedule_formset.is_valid() and schedule_deletion_formset.is_valid():
            instance_of_event = event_form.save()

            # sacing schedule_formset
            for schedule in schedule_formset:
                # pprint(repr(schedule))
                instance_of_schedule = schedule.save()
                instance_of_event.schedule_range.add(instance_of_schedule)


            for schedule_deletion in schedule_deletion_formset:
                print(schedule_deletion)
                '''
                WIP

                Delete checked schedule function is not working.
                WHY:
                I did put request.POST to formset initialization but it does not
                get any value at all.

                Need to google.
                '''



            return redirect('attendance:top', event_code=event.event_code)

        return HttpResponse('post has been sent')





    def get_event_form(self, request, instance=None, *args, **kwargs):
        form = EventModelForm(request.POST or None, instance=instance)
        return form

    def get_schedule_formset(self, request, extra=0, instance=None, *args, **kwargs):
        ScheduleFormSet = formset_factory(ScheduleModelForm, extra=extra)
        formset = ScheduleFormSet(request.POST or None, initial=instance)
        return formset



    def get_scheduledeletion_formset(self, request, extra=0, instance=None, *args, **kwargs):
        ScheduleDeletionCheckFormSet = formset_factory(ScheduleDeletionCheckModelForm, extra=extra)
        formset = ScheduleDeletionCheckFormSet(data=request.POST or None, initial=instance)
        return formset


    def get_schedule_list(self, event, *args, **kwargs):
        if event:
            schedule_list = []
            for schedule in event.schedule_range.all():
                # Creating schedule as a dict for schedule_formset instance
                tmp_dict = {
                    'id': schedule.id,
                    'date': schedule.date,
                    'comment': schedule.comment
                }
                schedule_list.append(tmp_dict)
        return schedule_list







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





# # UpdateEventView TEST
# class UpdateEventView(View):
#
#     template_name = 'create_event.html'
#
#     def get(self, request, pk=None, *args, **kwargs):
#         event = get_object_or_404(Event, pk=pk)
#         event_form = self.get_event_form(request, instance=event)
#         schedule_list = []
#         for schedule in event.schedule_range.all():
#             dictio = {
#                 'date': schedule.date,
#                 'comment': schedule.comment
#             }
#             print(dictio)
#             schedule_list.append(dictio)
#         print(schedule_list)
#
#         schedule_formset = self.get_schedule_formset(request, instance=schedule_list)
#         # schedule_formset = self.get_schedule_formset(request, instance=schedule_list)
#
#         context = {
#             'event_form': event_form,
#             'schedule_formset': schedule_formset
#         }
#         return render(request, self.template_name, context)
#
#         # return HttpResponse('update view')
#
#     def post(self, request, event_code=None, *args, **kwargs):
#         pass
#
#     def get_event_form(self, request, instance, *args, **kwargs):
#         form = EventModelForm(request.POST or None, instance=instance)
#         return form
#
#     def get_schedule_formset(self, request, extra=0, instance=None, *args, **kwargs):
#         ScheduleFormSet = formset_factory(ScheduleModelForm, extra=0)
#         formset = ScheduleFormSet(request.POST or None, initial=instance)
#
#         return formset
