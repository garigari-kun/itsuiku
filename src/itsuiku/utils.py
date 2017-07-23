
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template import loader

from django.core.mail import send_mail


def send_confirmation_email(request, user, form):
    pass




def post(self, request, *args, **kwargs):
    form = self.get_password_reset_request_form(request)
    if form.is_valid():
        email = form.cleaned_data['email']
        assoc_user = get_user_model().objects.get(email=email)
        if assoc_user:
            s_info = {
                'email': assoc_user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'itsuiku',
                'uid': urlsafe_base64_encode(force_bytes(assoc_user.id)),
                'user': assoc_user,
                'token': default_token_generator.make_token(assoc_user),
                'protocol': 'http'
            }
            mail_subject_template_name = 'user_settings/password_reset_subject.txt'
            mail_content_template_name = 'user_settings/password_reset_email.html'
            subject = loader.render_to_string(mail_subject_template_name, s_info)
            content = loader.render_to_string(mail_content_template_name, s_info)
            subject = ''.join(subject.splitlines())

            # send_mail(
            #     subject,
            #     content,
            #     DEFAULT_FROM_EMAIL ,
            #     [assoc_user.email],
            #     fail_silently=False
            # )
