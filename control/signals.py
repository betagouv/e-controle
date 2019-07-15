from django.dispatch import receiver

from .api_views import questionnaire_api_post_save
from .models import Questionnaire
from . import docx


@receiver(questionnaire_api_post_save, sender=Questionnaire)
def api_post_save_generate_questionnaire_file(instance, **kwargs):
    """
    Generate the questionnaire file after the API's save.
    This means that the file is generated every time the API post save signal
    is triggered - typically when the user saves a questionnaire.
    """
    questionnaire = instance
    docx.generate_questionnaire_file(questionnaire)
