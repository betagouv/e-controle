import os

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from django_cleanup import cleanup
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel
from softdelete.models import SoftDeleteModel

from soft_deletion.managers import DeletableQuerySet

from .docx import DocxMixin
from .upload_path import questionnaire_file_path, question_file_path, response_file_path, Prefixer

from user_profiles.models import UserProfile


class WithNumberingMixin(object):
    """
    Add an helper for getting the numbering base on the order field.
    """

    @property
    def numbering(self):
        return self.order + 1
    numbering.fget.short_description = 'Numérotation'


class FileInfoMixin(object):
    """
    Add common helpers for file information.
    """

    @property
    def file_name(self):
        return self.file.name

    def __str__(self):
        return f'id {self.id} - {self.file_name}'


class Control(SoftDeleteModel):
    # These error messages are used in the frontend (ConsoleCreate.vue),
    # if you change them you might break the frontend.
    INVALID_ERROR_MESSAGE = 'INVALID'
    UNIQUE_ERROR_MESSAGE = 'UNIQUE'

    title = models.CharField(
        "procédure",
        help_text="Procédure pour laquelle est ouvert cet espace de dépôt",
        max_length=255)
    depositing_organization = models.CharField(
        verbose_name="Organisme interrogé",
        help_text="Organisme qui va déposer les pièces dans cet espace de dépôt",
        max_length=255,
        blank=True,
    )
    reference_code = models.CharField(
        verbose_name="code de référence",
        max_length=255,
        help_text='Ce code est utilisé notamment pour le dossier de stockage des réponses',
        validators=[
            RegexValidator(
                regex='^[\.\s\w-]+$',
                message=INVALID_ERROR_MESSAGE,
            ),
        ],
        unique=True,
        error_messages={'unique': UNIQUE_ERROR_MESSAGE})

    objects = DeletableQuerySet.as_manager()

    class Meta:
        verbose_name = "Contrôle"
        verbose_name_plural = "Contrôles"

    def data(self):
        return {
            'id': self.id,
            'title': self.title,
            'depositing_organization': self.depositing_organization,
        }

    @property
    def next_questionnaire_numbering(self):
        if not self.questionnaires.exists():
            return 1
        return self.questionnaires.last().numbering + 1

    @property
    def has_multiple_inspectors(self):
        return self.user_profiles.filter(profile_type=UserProfile.INSPECTOR).count() > 1

    @property
    def title_display(self):
        if self.depositing_organization:
            return f'{self.title} - {self.depositing_organization}'
        return self.title

    def __str__(self):
        if self.depositing_organization:
            return f'id {self.id} - {self.title} - {self.depositing_organization}'
        return f'id {self.id} - {self.title}'


class Questionnaire(OrderedModel, WithNumberingMixin, DocxMixin):
    title = models.CharField("titre", max_length=255)
    sent_date = models.DateField(
        verbose_name="date d'envoie", blank=True, null=True,
        help_text="Date de transmission du questionnaire")
    end_date = models.DateField(
        verbose_name="échéance", blank=True, null=True,
        help_text="Date de réponse souhaitée")
    description = models.TextField("description", blank=True)
    editor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='questionnaires', on_delete=models.PROTECT,
        blank=True, null=True)
    uploaded_file = models.FileField(
        verbose_name="fichier du questionnaire", upload_to=questionnaire_file_path,
        null=True, blank=True,
        help_text=(
            "Si ce fichier est renseigné, il sera proposé au téléchargement."
            "Sinon, un fichier généré automatiquement sera disponible."))
    generated_file = models.FileField(
        verbose_name="fichier du questionnaire généré automatiquement",
        upload_to=questionnaire_file_path,
        null=True, blank=True,
        help_text=(
            "Ce fichier est généré automatiquement quand le questionnaire est enregistré."))
    control = models.ForeignKey(
        to='Control', verbose_name='contrôle', related_name='questionnaires',
        null=True, blank=True, on_delete=models.CASCADE)
    order_with_respect_to = 'control'
    order = models.PositiveIntegerField('order', db_index=True)
    is_draft = models.BooleanField(
        verbose_name="brouillon", default=False,
        help_text="Ce questionnaire est-il encore au stade de brouillon?")
    modified = models.DateTimeField('modifié', auto_now=True, null=True)

    class Meta:
        ordering = ('control', 'order')
        verbose_name = "Questionnaire"
        verbose_name_plural = "Questionnaires"

    @property
    def file(self):
        """
        If there is a manually uplodaed file it will take precedence.
        """
        if bool(self.uploaded_file):
            return self.uploaded_file
        return self.generated_file

    @property
    def url(self):
        return reverse('questionnaire-detail', args=[self.id])

    @property
    def file_url(self):
        return reverse('send-questionnaire-file', args=[self.id])

    @property
    def basename(self):
        """
        Name of file, without path.
        """
        return os.path.basename(self.file.name)

    @property
    def title_display(self):
        return f"Questionnaire n°{self.numbering} - {self.title}"

    @property
    def end_date_display(self):
        if not self.end_date:
            return None
        return self.end_date.strftime("%A %d %B %Y")

    @property
    def description_rich_text(self):
        return self.to_rich_text(self.description)

    def __str__(self):
        return f'id {self.id} - C{self.control.id}-Q{self.numbering} - {self.title}'


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

    @property
    def control(self):
        return self.questionnaire.control

    def __str__(self):
        return f'id {self.id} - C{self.questionnaire.control.id}-Q{self.questionnaire.numbering}-T{self.numbering} - {self.title}'


class Question(OrderedModel, WithNumberingMixin, DocxMixin):
    description = models.TextField("description")
    theme = models.ForeignKey(
        'theme', verbose_name='thème', related_name='questions',
        null=True, blank=True, on_delete=models.CASCADE)
    order_with_respect_to = 'theme'

    class Meta:
        ordering = ('theme', 'order')
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    @property
    def control(self):
        return self.theme.control

    @property
    def questionnaire(self):
        return self.theme.questionnaire

    @property
    def description_rich_text(self):
        return self.to_rich_text(self.description)

    def __str__(self):
        return f'id {self.id} - C{self.theme.questionnaire.control.id}-Q{self.theme.questionnaire.numbering}-T{self.theme.numbering}-{self.numbering} - {self.description}'


class QuestionFile(OrderedModel, FileInfoMixin):
    question = models.ForeignKey(
        to='Question', verbose_name='question', related_name='question_files',
        on_delete=models.CASCADE)
    file = models.FileField(verbose_name="fichier", upload_to=question_file_path)
    order_with_respect_to = 'question'

    class Meta:
        ordering = ('question', 'order')
        verbose_name = 'Question: Fichier Annexe'
        verbose_name_plural = 'Question: Fichiers Annexes'

    @property
    def control(self):
        return self.question.control

    @property
    def questionnaire(self):
        return self.question.questionnaire

    @property
    def url(self):
        return reverse('send-question-file', args=[self.id])

    @property
    def basename(self):
        """
        Name of file, without path.
        """
        return os.path.basename(self.file.name)


@cleanup.ignore
class ResponseFile(TimeStampedModel, FileInfoMixin):
    question = models.ForeignKey(
        to='Question', verbose_name='question', related_name='response_files',
        on_delete=models.CASCADE)
    file = models.FileField(verbose_name="fichier", upload_to=response_file_path)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='response_files', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(
        verbose_name="Supprimé", default=False,
        help_text="Ce fichier est=il dans la corbeille?")

    class Meta:
        verbose_name = 'Réponse: Fichier Déposé'
        verbose_name_plural = 'Réponse: Fichiers Déposés'

    @property
    def url(self):
        return reverse('send-response-file', args=[self.id])

    @property
    def basename(self):
        """
        Name of file, without path and without name prefix.
        """
        prefixer = Prefixer(self)
        if self.is_deleted:
            return prefixer.strip_deleted_file_prefix()
        return prefixer.strip_file_prefix()
