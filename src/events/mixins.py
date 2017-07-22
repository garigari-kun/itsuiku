from events.models import Event

class EventOwnerMixin(object):
    def dispatch(self, request, id=None, *args, **kwargs):
        event = get_object_or_404(Event, id=id)
        if event.user.id == request.user.id:
            return super(EventOwnerMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404()




class SuperuserRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(SuperuserRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404()
