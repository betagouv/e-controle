from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail as django_send_mail
from django.template import loader


current_site = Site.objects.get_current()


def send_email(
        subject, text_template, html_template, recipient_list,
        from_email=settings.DEFAULT_FROM_EMAIL, extra_context=None):
    context = {'site': current_site}
    if extra_context:
        context.update(extra_context)
    text_message = loader.render_to_string(text_template, context)
    html_message = loader.render_to_string(html_template, context)
    return django_send_mail(
        subject=subject,
        message=text_message,
        from_email=from_email,
        html_message=html_message,
        recipient_list=recipient_list,
        fail_silently=False,
    )
