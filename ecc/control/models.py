from django.db import models
from django.urls import reverse

from filer.fields.file import FilerFileField
from mptt.models import MPTTModel, TreeForeignKey
from ordered_model.models import OrderedModel

from .upload_path import response_file_path


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


class Questionnaire(OrderedModel):
    title = models.CharField("titre", max_length=255)
    reference_code = models.CharField(
        verbose_name="code de référence", max_length=255, blank=True,
        help_text='Ce code est utilisé notamment pour le dossier de stockage des réponses')
    end_date = models.DateField("échéance", blank=True, null=True)
    description = models.TextField("description", blank=True)
    control = models.ForeignKey(
        to='Control', verbose_name='controle', related_name='questionnaires',
        null=True, blank=True, on_delete=models.CASCADE)
    order_with_respect_to = 'control'

    class Meta:
        ordering = ('order',)
        verbose_name = "Questionnaire"
        verbose_name_plural = "Questionnaires"

    @property
    def url(self):
        return reverse('questionnaire-detail', args=[self.id])

    def __str__(self):
        return self.title


class Theme(MPTTModel):
    title = models.CharField("titre", max_length=255)
    reference_code = models.CharField(
        verbose_name="code de référence", max_length=255, blank=True,
        help_text='Ce code est utilisé notamment pour le dossier de stockage des réponses')
    parent = TreeForeignKey(
        to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    questionnaire = models.ForeignKey(
        to='Questionnaire', verbose_name='questionnaire', related_name='themes',
        null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"

    def __str__(self):
        return self.title


class Question(OrderedModel):
    description = models.TextField("description", max_length=255)
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
        to='Question', verbose_name='question', related_name='files', on_delete=models.CASCADE)
    file = FilerFileField(verbose_name="fichier", on_delete=models.CASCADE)
    order_with_respect_to = 'question'

    class Meta:
        verbose_name = 'Fichier Attaché'
        verbose_name_plural = 'Fichiers Attachés'


class ResponseFile(models.Model):
    question = models.ForeignKey(
        to='Question', verbose_name='question', related_name='question',
        on_delete=models.CASCADE)
    file = models.FileField(verbose_name="fichier", upload_to=response_file_path)

    class Meta:
        verbose_name = 'Fichier Réponse Attaché'
        verbose_name_plural = 'Fichiers Réponse Attachés'
