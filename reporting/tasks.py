from datetime import timedelta

from actstream import action
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone


from celery import task
from celery.utils.log import get_task_logger

from control.models import Control, ResponseFile


logger = get_task_logger(__name__)

current_site = Site.objects.get_current()


def send_ecc_email(subject, text_template, html_template, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL, extra_context=None):
    context = {'site': current_site}
    if extra_context:
        context.update(extra_context)
    text_message = loader.render_to_string(text_template, context)
    html_message = loader.render_to_string(html_template, context)
    return send_mail(
        subject=subject,
        message=text_message,
        from_email=from_email,
        html_message=html_message,
        recipient_list=recipient_list,
        fail_silently=False,
    )


@task
def send_files_report():
    html_template = 'reporting/email/files_report.html'
    text_template = 'reporting/email/files_report.txt'
    for control in Control.objects.all():
        logger.info(f'Processing control: {control}')
        subject = f'{control.reference_code} - de nouveaux documents déposés !'
        latest_email_sent = control.actor_actions.filter(verb='sent-files-report').first()
        if latest_email_sent:
            date_cutoff = latest_email_sent.timestamp
        else:
            date_cutoff = timezone.now() - timedelta(hours=24)
        logger.info(f"Looking for files uploaded after this timestamp: {date_cutoff}")
        files = ResponseFile.objects.filter(
            question__theme__questionnaire__control=control,
            created__gt=date_cutoff,
        )
        logger.info(f'Number of files: {len(files)}')
        if not files:
            return None
        recipients = control.user_profiles.filter(send_files_report=True)
        recipient_list = recipients.values_list('user__email', flat=True)
        logger.info(f'Recipients: {recipient_list}')

        if not recipient_list:
            return None
        context = {'files': files}
        number_of_sent_email = send_ecc_email(
            subject=subject,
            text_template=text_template,
            html_template=html_template,
            recipient_list=recipient_list,
            extra_context=context,
        )
        logger.info(f"Sent {number_of_sent_email} emails")
        number_of_recipients = len(recipient_list)
        if number_of_sent_email != number_of_recipients:
            logger.warning(
                "There was {number_of_recipients} recipients, "
                "but {number_of_sent_email} email(s) sent.")
        logger.info(f'Email sent for {control}')
        action.send(sender=control, verb='sent-files-report')
