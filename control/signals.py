import ntpath
import os


from django.conf import settings
from django.dispatch import receiver
from django.utils.text import slugify

from docxtpl import DocxTemplate, RichText

from .api_views import questionnaire_api_post_save
from .models import Questionnaire
from .upload_path import questionnaire_file_path


@receiver(questionnaire_api_post_save, sender=Questionnaire)
def generate_questionnaire_file(instance, **kwargs):
    questionnaire = instance
    doc = DocxTemplate("templates/ecc/questionnaire.docx")
    context = {
        'questionnaire': questionnaire,
        'description': RichText(questionnaire.description)
    }
    doc.render(context)
    filename = f'{slugify(questionnaire.title)}.docx'
    # Why do we need both relative and absolte path?
    # For django's FileField, we need a relative path from the root of the MEDIA_ROOT.
    # For saving the file via DocxTemplate, we need to absolute path.
    relative_path = questionnaire_file_path(questionnaire, filename)
    absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)
    file_folder = ntpath.split(absolute_path)[0]
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    doc.save(absolute_path)
    questionnaire.generated_file = relative_path
    questionnaire.save()
