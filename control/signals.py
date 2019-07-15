import os

from django.dispatch import receiver
from django.conf import settings

from .api_views import questionnaire_api_post_save
from .models import Questionnaire
from .upload_path import questionnaire_path


@receiver(questionnaire_api_post_save, sender=Questionnaire)
def create_questionnaire_path(instance, **kwargs):
    """
    Create the questionnaire folder after the API's save.
    """
    questionnaire = instance
    relative_path = questionnaire_path(questionnaire)
    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    if not os.path.exists(absolute_path):
        os.makedirs(absolute_path)
