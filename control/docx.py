import ntpath
import os


from django.conf import settings
from django.utils.text import slugify

from docxtpl import DocxTemplate, RichText

from .upload_path import questionnaire_file_path


def generate_questionnaire_file(questionnaire):
    """
    Generate a word Docx document for the given questionnaire.
    The generated docment is based on a Docx template.
    This is made possible thanks to docxtepl Python package.
    """
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
