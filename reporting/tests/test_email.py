from pytest import mark

from django.contrib.auth import get_user_model
from django.core import mail

from reporting.tasks import send_files_report
from tests import factories
from user_profiles.models import UserProfile


pytestmark = mark.django_db

User = get_user_model()


def test_email_is_sent_if_there_is_a_response_file():
    response_file = factories.ResponseFileFactory()
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    inspector.controls.add(response_file.question.theme.questionnaire.control)
    inspector.send_files_report = True
    inspector.save()
    count_emails_before = len(mail.outbox)
    send_files_report()
    count_emails_after = len(mail.outbox)
    assert count_emails_after == count_emails_before + 1


def test_email_is_not_sent_if_sending_flag_is_disabled():
    response_file = factories.ResponseFileFactory()
    inspector = factories.UserProfileFactory(profile_type=UserProfile.INSPECTOR)
    inspector.controls.add(response_file.question.theme.questionnaire.control)
    inspector.send_files_report = False
    inspector.save()
    count_emails_before = len(mail.outbox)
    send_files_report()
    count_emails_after = len(mail.outbox)
    assert count_emails_after == count_emails_before
