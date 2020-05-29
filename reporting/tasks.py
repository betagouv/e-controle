import logging
import time
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from actstream import action
from celery import task
from celery.utils.log import get_task_logger

from control.models import Control, ResponseFile
from utils.email import send_email


logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


ACTION_LOG_VERB_SENT = 'files report email sent'
ACTION_LOG_VERB_NOT_SENT = 'files report email not sent'


def get_date_cutoff(control):
    """
    The reporting tool looks for files uploaded after a certain date cutoff, which could be :
    - The last thime a reporting email was sent
    - 24h from now
    """
    latest_email_sent = control.actor_actions.filter(verb=ACTION_LOG_VERB_SENT).first()
    if latest_email_sent:
        date_cutoff = latest_email_sent.timestamp
    else:
        date_cutoff = timezone.now() - timedelta(hours=24)
    return date_cutoff


def get_files(control):
    date_cutoff = get_date_cutoff(control)
    logger.info("Looking for files uploaded after this timestamp: {}".format(
        date_cutoff.strftime("%Y-%m-%d %H:%M:%S")))
    files = ResponseFile.objects.filter(
        question__theme__questionnaire__control=control,
        created__gt=date_cutoff,
    )
    logger.info(f'Number of files: {len(files)}')
    return files


@task
def send_files_report():
    html_template = 'reporting/email/files_report.html'
    text_template = 'reporting/email/files_report.txt'
    for control in Control.objects.all():
        logger.info(f'Processing control: {control.id}')
        if control.depositing_organization:
            subject = control.depositing_organization
        else:
            subject = control.title
        subject += ' - de nouveaux documents déposés !'
        files = get_files(control)
        if not files:
            logger.info(f'No new documents, aborting.')
            continue
        recipients = control.user_profiles.filter(send_files_report=True)
        recipient_list = recipients.values_list('user__email', flat=True)
        if not recipient_list:
            logger.info(f'No recipients, aborting.')
            continue
        logger.debug(f'Recipients: {len(recipient_list)}')
        date_cutoff = get_date_cutoff(control)
        context = {
            'control': control,
            'date_cutoff': date_cutoff.strftime("%A %d %B %Y"),
            'files': files,
        }
        number_of_sent_email = send_email(
            to=recipient_list,
            subject=subject,
            html_template=html_template,
            text_template=text_template,
            extra_context=context,
        )
        logger.info(f"Sent {number_of_sent_email} emails")
        number_of_recipients = len(recipient_list)
        if number_of_sent_email != number_of_recipients:
            logger.warning(
                f'There was {number_of_recipients} recipient(s), '
                f'but {number_of_sent_email} email(s) sent.')
        if number_of_sent_email > 0:
            logger.info(f'Email sent for control {control.id}')
            action.send(sender=control, verb=ACTION_LOG_VERB_SENT)
        else:
            logger.info(f'No email was sent for control {control.id}')
            action.send(sender=control, verb=ACTION_LOG_VERB_NOT_SENT)

        EMAIL_SPACING_TIME_SECONDS = settings.EMAIL_SPACING_TIME_MILLIS / 1000
        logger.info(
            f'Waiting {EMAIL_SPACING_TIME_SECONDS}s after emailing for control {control.id}')
        time.sleep(EMAIL_SPACING_TIME_SECONDS)
