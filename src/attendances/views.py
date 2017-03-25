from django.shortcuts import get_object_or_404, render

from events.models import Event

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
