from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template import loader
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


def send_confirmation_email(request, user=None, subject_template=None, content_template=None):
    """ Utility method for sending confirmation email
    Return True if the email was sent to the user
    Return False if the user is None
    """
    if user:
        s_info = {
            'email': user.email,
            'domain': request.META['HTTP_HOST'],
            'site_name': 'itsuiku',
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http'
        }
        mail_subject_template_name = subject_template
        mail_content_template_name = content_template
        subject = loader.render_to_string(mail_subject_template_name, s_info)
        content = loader.render_to_string(mail_content_template_name, s_info)
        subject = ''.join(subject.splitlines())
        print(content)
        print(subject)
        # send_mail(
        #     subject,
        #     content,
        #     DEFAULT_FROM_EMAIL ,
        #     [user.email],
        #     fail_silently=False
        # )
        return True
    else:
        return False


def send_contact_email(request, contact=None, subject_template=None, content_template=None):
    """ Utility method for sendinf contact email to me
    Return True if the email was sent to the user
    Return False if the email was not sent to the user
    """
    if contact:
        subject = loader.render_to_string(subjecte_template, context)
        content = loader.render_to_string(content_template, context)
        subject = ''.join(subject.splitlines())
        # send_mail = (
        #     subject,
        #     content,
        #     DEFAULT_FROM_EMAIL,
        #     ADMIN_EMAIL,
        #     fail_silently=False
        # )
        return True
    else:
        return False




def check_visitor_is_events_owner(request, event):
    if request.user == event.user:
        return True
    else:
        return False
