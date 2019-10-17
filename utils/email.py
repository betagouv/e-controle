from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import loader


current_site = Site.objects.get_current()


def send_email(
        to, cc, subject, text_template, html_template,
        from_email=settings.DEFAULT_FROM_EMAIL, extra_context=None):
    context = {'site': current_site}
    if extra_context:
        context.update(extra_context)
    text_message = loader.render_to_string(text_template, context)
    html_message = loader.render_to_string(html_template, context)
    email = EmailMultiAlternatives(
        to=to,
        cc=cc,
        subject=subject,
        body=text_message,
        from_email=from_email,
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
