from django.conf import settings
from django.db import models
from django.urls import reverse

from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel


from .upload_path import question_file_path, response_file_path


class WithNumberingMixin(object):
    """
    Add an helper method for getting the numbering base on the order field.
    """

    @property
    def numbering(self):
        return self.order + 1
    numbering.fget.short_description = 'Numérotation'


class Control(models.Model):
    title = models.CharField("title", max_length=255)
    reference_code = models.CharField(
        verbose_name="code de référence", max_length=255, blank=True,
        help_text='Ce code est utilisé notamment pour le dossier de stockage des réponses')

    class Meta:
        verbose_name = "Controle"
        verbose_name_plural = "Controles"

    def __str__(self):
        return self.title


class Questionnaire(OrderedModel, WithNumberingMixin):
    title = models.CharField("titre", max_length=255)
    end_date = models.DateField("échéance", blank=True, null=True)
    description = models.TextField("description", blank=True)
    control = models.ForeignKey(
        to='Control', verbose_name='controle', related_name='questionnaires',
        null=True, blank=True, on_delete=models.CASCADE)
    order_with_respect_to = 'control'

    class Meta:
        ordering = ('control', 'order')
        verbose_name = "Questionnaire"
        verbose_name_plural = "Questionnaires"

    @property
    def url(self):
        return reverse('questionnaire-detail', args=[self.id])

    def __str__(self):
        return self.title


class Theme(OrderedModel, WithNumberingMixin):
    title = models.CharField("titre", max_length=255)
    questionnaire = models.ForeignKey(
        to='Questionnaire', verbose_name='questionnaire', related_name='themes',
        null=True, blank=True, on_delete=models.CASCADE)
    order_with_respect_to = 'questionnaire'

    class Meta:
        ordering = ('questionnaire', 'order')
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"

    def __str__(self):
        return self.title


class Question(OrderedModel, WithNumberingMixin):
    description = models.TextField("description")
    theme = models.ForeignKey(
        'theme', verbose_name='thème', related_name='questions', on_delete=models.CASCADE)
    order_with_respect_to = 'theme'

    class Meta:
        ordering = ('theme', 'order')
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.description


class QuestionFile(OrderedModel):
    question = models.ForeignKey(
        to='Question', verbose_name='question', related_name='question_files',
        on_delete=models.CASCADE)
    file = models.FileField(verbose_name="fichier", upload_to=question_file_path)
    order_with_respect_to = 'question'

    class Meta:
        ordering = ('question', 'order')
        verbose_name = 'Question: Fichier Attaché'
        verbose_name_plural = 'Question: Fichiers Attachés'

    @property
    def url(self):
        return reverse('send-question-file', args=[self.id])

    def __str__(self):
        return self.file.name


class ResponseFile(TimeStampedModel):
    question = models.ForeignKey(
        to='Question', verbose_name='question', related_name='response_files',
        on_delete=models.CASCADE)
    file = models.FileField(verbose_name="fichier", upload_to=response_file_path)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='response_files', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Réponse: Fichier Attaché'
        verbose_name_plural = 'Réponse: Fichiers Attachés'

    @property
    def url(self):
        return reverse('send-response-file', args=[self.id])

    def __str__(self):
        return self.file.name
