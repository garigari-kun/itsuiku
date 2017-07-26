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



class ForumView(View):

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_name(request), self.get_context_data(request))

    def get_template_name(self, request, *args, **kwargs):
        template_name = 'home/forum.html'
        return template_name

    def get_context_data(self, request, *args, **kwargs):
        context = {}
        return context




class ContactFormView(View):

    def get(self, request, *args, **kwargs):
        template_name = self.get_template_name(request, form_valid=False)
        context = self.get_context_data(request)
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        contact_form = self.get_contact_form(request)
        if contact_form.is_valid():
            email = contact_form.cleaned_data['email']
            url = contact_form.cleaned_data['url']
            content = contact_form.cleaned_data['content']
            category = contact_form.cleaned_data['category']
            return render(request, self.get_template_name(request, form_valid=True), {})
        else:
            return render(request, self.get_template_name(request, form_valid=False), self.get_context_data(request))

    def get_context_data(self, request):
        context = {}
        context['contact_form'] = self.get_contact_form(request)
        return context

    def get_template_name(self, request, *args, **kwargs):
        if kwargs['form_valid'] == True:
            template_name = 'home/sent_contact.html'
        else:
            template_name = 'home/contact.html'
        return template_name

    def get_contact_form(self, request):
        form = ContactForm(request.POST or None)
        return form
