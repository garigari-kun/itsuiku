
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.forms import formset_factory

from events.models import Event
from invitees.forms import InviteeModelForm, AttendanceModelForm

class EventTopView(View):
    # test event code : dcmqrez5b591
    def get(self, request, event_code=None, *args, **kwargs):
        template_name = 'events/event-top.html'
        event = get_object_or_404(Event, event_code=event_code)
        print(len(event.schedule_range.all()))
        num_of_date = len(event.schedule_range.all())
        # attendance_form = AttendanceModelForm()
        AttendanceFormSet = formset_factory(AttendanceModelForm, extra=num_of_date)
        attendance_form = AttendanceFormSet()

        context = {
            'event': event,
            'attendance_form': attendance_form,
        }
        return render(request, template_name, context)
