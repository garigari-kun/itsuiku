from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
from django.forms import formset_factory

from events.models import Event
from user_settings.models import UserProfile
from invitees.models import Invitee, Attendance
from invitees.forms import InviteeModelForm, AttendanceModelForm

from itsuiku.utils import check_visitor_is_events_owner



class EventTopView(View):

    template_name = 'events/event-top.html'


    def get(self, request, event_code=None, *args, **kwargs):
        context = self.get_context_data(request, event_code=event_code)
        event = Event.objects.get(event_code=event_code)
        return render(request, self.template_name, context)


    def get_context_data(self, request, event_code=None, *args, **kwargs):
        context = {}
        context['event'] = get_object_or_404(Event, event_code=event_code)
        context['invitees'] = Invitee.objects.filter(event=context['event'])
        context['schedule_range'] = context['event'].schedule_range.all()
        context['user_profile'] = UserProfile.objects.get_user_profile(request, user=context['event'].user)
        context['is_owner'] = check_visitor_is_events_owner(request, context['event'])
        return context









class CreateEventAttendanceView(View):

    template_name = 'events/create-event-attendance.html'

    def get(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        num_of_date = len(event.schedule_range.all())
        # Entered invitees
        # invitees = Invitee.objects.filter(event=event)
        invitee_form = self.get_invitee_form(request)
        attendance_form = self.get_attendance_formset(request, extra=num_of_date)
        schedule_list = event.schedule_range.all()
        # Zipped schedule_list and attendance_form
        sl_af = zip(schedule_list, attendance_form)


        context = {
            'event': event,
            'attendance_form': attendance_form,
            'invitee_form': invitee_form,
            'sl_af': sl_af
        }
        return render(request, self.template_name, context)


    def post(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        # InviteeModelForm
        invitee_form = self.get_invitee_form(request)
        # AttendanceModelFormSet
        attendance_form = self.get_attendance_formset(request)
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
        return HttpResponse('something bad thing was happend.')

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
        attendance_list = self.get_attendance_list(invitee)
        invitee_form = self.get_invitee_form(request, instance=invitee)
        attendance_form = self.get_attendance_formset(request, instance=attendance_list)
        schedule_list = event.schedule_range.all()
        # Zipped schedule_list and attendance_form
        sl_af = zip(schedule_list, attendance_form)


        context = {
            'event': event,
            'attendance_form': attendance_form,
            'invitee_form': invitee_form,
            'sl_af': sl_af
        }
        return render(request, self.template_name, context)


    """
    WIP:

    I'm implementing that deleting older Attendance record instead of updating, because
    I could not find a way to do that so I need to research that later.


    """
    def post(self, request, event_code=None, invitee_id=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        invitee = get_object_or_404(Invitee, pk=invitee_id)

        invitee_form = self.get_invitee_form(request, instance=invitee)
        attendance_list = self.get_attendance_list(invitee)
        attendance_form = self.get_attendance_formset(request, instance=attendance_list)

        if invitee_form.is_valid() and attendance_form.is_valid():
            instance_invitee = invitee_form.save()

            for (attendance, schedule) in zip(attendance_form, event.schedule_range.all()):
                instance_attendance = attendance.save(commit=False)
                instance_attendance.schedule = schedule
                instance_attendance.event = event
                instance_attendance.save()
                instance_invitee.attendance.add(instance_attendance)

            # Delete older Attendance record
            for d_attendance in attendance_list:
                result = Attendance.objects.filter(id=d_attendance['id']).delete()

            return redirect('attendance:top', event_code=event_code)

        else:
            return HttpResponse('form is invalid')

        return HttpResponse('post has been sent')



    def get_invitee_form(self, request, instance,  *args, **kwargs):
        form = InviteeModelForm(request.POST or None, instance=instance)
        return form

    def get_attendance_formset(self, request, extra=0, instance=None, *args, **kwargs):
        AttendanceFormSet = formset_factory(AttendanceModelForm, extra=extra)
        form = AttendanceFormSet(request.POST or None, initial=instance)
        return form


    def get_attendance_list(self, invitee):
        attendance_list = []
        for attendance in invitee.attendance.all():
            tmp_dict = {
                'id': attendance.id,
                'choice': attendance.choice,
            }
            attendance_list.append(tmp_dict)
        return attendance_list








class DeleteEventAttendanceView(View):

    def get(self, request, event_code=None, invitee_id=None, *args, **kwargs):
        invitee = get_object_or_404(Invitee, pk=invitee_id)
        # Delete Attendance records
        for attendance in invitee.attendance.all():
            attendance.delete()
        # Delete Invitee record
        invitee.delete()
        return redirect('attendance:top', event_code=event_code)










#
