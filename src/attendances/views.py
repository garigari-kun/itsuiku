from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
from django.forms import formset_factory

from events.models import Event
from invitees.models import Invitee
from invitees.forms import InviteeModelForm, AttendanceModelForm

class EventTopView(View):
    # test event code : dcmqrez5b591
    def get(self, request, event_code=None, *args, **kwargs):
        template_name = 'events/event-top.html'
        event = get_object_or_404(Event, event_code=event_code)
        num_of_date = len(event.schedule_range.all())

        # Entered invitees
        invitees = Invitee.objects.filter(event=event)



        # InviteeModelForm
        invitee_form = InviteeModelForm()
        # AttendanceModelFormSet
        AttendanceFormSet = formset_factory(AttendanceModelForm, extra=num_of_date)
        attendance_form = AttendanceFormSet()

        context = {
            'event': event,
            'invitees': invitees,
            'attendance_form': attendance_form,
            'invitee_form': InviteeModelForm,
        }
        return render(request, template_name, context)


    def post(self, request, event_code=None, *args, **kwargs):
        event = get_object_or_404(Event, event_code=event_code)
        # InviteeModelForm
        invitee_form = InviteeModelForm(request.POST)
        # AttendanceModelFormSet
        AttendanceFormSet = formset_factory(AttendanceModelForm)
        attendance_form = AttendanceFormSet(request.POST)
        if invitee_form.is_valid() and attendance_form.is_valid():
            print('both valid')
            instance_invitee = invitee_form.save(commit=False)
            instance_invitee.event = event
            instance_invitee.save()

            for (attendance, schedule) in zip(attendance_form, event.schedule_range.all()):
                print(attendance)
                print(schedule)
                instance_attendance = attendance.save(commit=False)
                instance_attendance.schedule = schedule
                instance_attendance.event = event
                instance_attendance.save()
                instance_invitee.attendance.add(instance_attendance)


            return redirect('attendance:top', event_code=event_code)

        else:
            print('both invalid')
        return HttpResponse('post has been sent')
