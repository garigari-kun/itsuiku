from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
from django.forms import formset_factory

from events.models import Event
from invitees.models import Invitee
from invitees.forms import InviteeModelForm, AttendanceModelForm

class EventTopView(View):

    template_name = 'events/event-top.html'


    def get(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        num_of_date = len(event.schedule_range.all())

        # Entered invitees
        invitees = Invitee.objects.filter(event=event)

        # invitee_form = self.get_invitee_form(request)
        # attendance_form = self.get_attendance_formset(request, extra=num_of_date)

        context = {
            'event': event,
            'invitees': invitees,
            # 'attendance_form': attendance_form,
            # 'invitee_form': InviteeModelForm,
        }
        return render(request, self.template_name, context)


    def post(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        # InviteeModelForm
        invitee_form = InviteeModelForm(request.POST)
        # AttendanceModelFormSet
        AttendanceFormSet = formset_factory(AttendanceModelForm)
        attendance_form = AttendanceFormSet(request.POST)
        if invitee_form.is_valid() and attendance_form.is_valid():
            instance_invitee = invitee_form.save(commit=False)
            instance_invitee.event = event
            instance_invitee.save()

            for (attendance, schedule) in zip(attendance_form, event.schedule_range.all()):
                instance_attendance = attendance.save(commit=False)
                instance_attendance.schedule = schedule
                instance_attendance.event = event
                instance_attendance.save()
                instance_invitee.attendance.add(instance_attendance)

            return redirect('attendance:top', event_code=event_code)

        else:
            print('both invalid')
        return HttpResponse('post has been sent')


    def get_invitee_form(self, request, *args, **kwargs):
        form = InviteeModelForm(request.POST or None)
        return form

    def get_attendance_formset(self, request, extra=0, *args, **kwargs):
        AttendanceFormSet = formset_factory(AttendanceModelForm, extra=extra)
        form = AttendanceFormSet(request.POST or None)
        return form







class CreateEventAttendanceView(View):

    template_name = 'events/create-event-attendance.html'

    def get(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        num_of_date = len(event.schedule_range.all())

        # Entered invitees
        # invitees = Invitee.objects.filter(event=event)

        invitee_form = self.get_invitee_form(request)
        attendance_form = self.get_attendance_formset(request, extra=num_of_date)

        context = {
            'event': event,
            # 'invitees': invitees,
            'attendance_form': attendance_form,
            'invitee_form': invitee_form,
        }
        return render(request, self.template_name, context)


    def post(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        # InviteeModelForm
        invitee_form = InviteeModelForm(request.POST)
        # AttendanceModelFormSet
        AttendanceFormSet = formset_factory(AttendanceModelForm)
        attendance_form = AttendanceFormSet(request.POST)
        if invitee_form.is_valid() and attendance_form.is_valid():
            instance_invitee = invitee_form.save(commit=False)
            instance_invitee.event = event
            instance_invitee.save()

            for (attendance, schedule) in zip(attendance_form, event.schedule_range.all()):
                instance_attendance = attendance.save(commit=False)
                instance_attendance.schedule = schedule
                instance_attendance.event = event
                instance_attendance.save()
                instance_invitee.attendance.add(instance_attendance)

            return redirect('attendance:top', event_code=event_code)

        else:
            print('both invalid')
        return HttpResponse('post has been entered')

    def get_invitee_form(self, request, *args, **kwargs):
        form = InviteeModelForm(request.POST or None)
        return form

    def get_attendance_formset(self, request, extra=0, *args, **kwargs):
        AttendanceFormSet = formset_factory(AttendanceModelForm, extra=extra)
        form = AttendanceFormSet(request.POST or None)
        return form




class UpdateEventAttendanceView(View):

    template_name = 'events/create-event-attendance.html'

    def get(self, request, event_code=None, invitee_id=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        num_of_date = len(event.schedule_range.all())

        # Entered invitees
        invitee = get_object_or_404(Invitee, pk=invitee_id)

        attendance_list = []
        for attendance in invitee.attendance.all():
            tmp_dict = {
                'choice': attendance.choice
            }
            attendance_list.append(tmp_dict)


        invitee_form = self.get_invitee_form(request, instance=invitee)
        attendance_form = self.get_attendance_formset(request, extra=num_of_date, instance=attendance_list)
        #
        context = {
            'event': event,
            # 'invitees': invitees,
            'attendance_form': attendance_form,
            'invitee_form': invitee_form,
        }
        return render(request, self.template_name, context)
        # return HttpResponse('get request')


    def get_invitee_form(self, request, instance,  *args, **kwargs):
        form = InviteeModelForm(request.POST or None, instance=instance)
        return form

    def get_attendance_formset(self, request, extra=0, instance=None, *args, **kwargs):
        AttendanceFormSet = formset_factory(AttendanceModelForm, extra=extra)
        form = AttendanceFormSet(request.POST or None, initial=instance)
        return form



"""
        for schedule in event.schedule_range.all():
            # Creating schedule as a dict for schedule_formset instance
            tmp_dict = {
                'date': schedule.date,
                'comment': schedule.comment
            }
            schedule_list.append(tmp_dict)
        schedule_formset = self.get_schedule_formset(request, instance=schedule_list)
"""



















#
