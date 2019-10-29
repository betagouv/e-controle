from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from actstream import action


current_site = Site.objects.get_current()


def add_log_entry(site, verb, to, cc, subject, error=''):
    log_message = f'Sending email "{subject}" to: {to}.'
    if cc:
        log_message += f' Email CC: {cc}.'
    if error:
        log_message += f' Failed with error: {error}'
    action_details = {
        'sender': site,
        'verb': verb,
        'description': log_message,
    }
    action.send(**action_details)


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
    try:
        email.send(fail_silently=False)
        add_log_entry(site=current_site, verb='email sent', to=to, cc=cc, subject=subject)
    except Exception as e:
        add_log_entry(
            site=current_site, verb='email not sent', to=to, cc=cc, subject=subject,
            error=str(e))
