from django.shortcuts import render
from django.views.generic.base import View

from .forms import ContactForm

class TopView(View):


    def get(self, request, *args, **kwargs):
        context = self.get_context(request)
        template_name = self.get_template_name(request)
        return render(request, template_name, context)

    def get_context(self, request, *args, **kwargs):
        context = {}
        return context

    def get_template_name(self, request, *args, **kwargs):
        template_name = 'home/index.html'
        return template_name




class ContactFormView(View):

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request)
        context = self.get_context_data(request)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, request):
        context = {}
        context['contact_form'] = self.get_contact_form(request)
        return context

    def get_template_name(self, request):
        template_name = 'home/contact.html'
        return template_name

    def get_contact_form(self, request):
        form = ContactForm(request.POST or None)
        return form
