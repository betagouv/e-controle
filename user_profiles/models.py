from django.conf import settings
from django.db import models
from django.apps import apps

from annoying.fields import AutoOneToOneField
from fernet_fields import EncryptedCharField, EncryptedEmailField

from .managers import UserProfileQuerySet


class UserProfile(models.Model):
    AUDITED = 'audited'
    INSPECTOR = 'inspector'
    PROFILE_TYPE = (
        (AUDITED, 'Organisme interrogé'),
        (INSPECTOR, 'Contrôleur'),
    )
    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
        related_name='profile')
    first_name = EncryptedCharField(max_length=255, verbose_name='prénom', default='')
    last_name = EncryptedCharField(max_length=255, verbose_name='nom', default='')
    email = EncryptedEmailField(default='')
    profile_type = models.CharField(max_length=255, choices=PROFILE_TYPE)
    controls = models.ManyToManyField(
        to='control.Control', verbose_name='controles', related_name='user_profiles', blank=True)
    organization = models.CharField("Organisme", max_length=255, blank=True, null=True)
    send_files_report = models.BooleanField(
        verbose_name="Envoie Rapport de Fichiers", default=False,
        help_text="Envoyer par email le rapport des fichiers uplodés ?")
    agreed_to_tos = models.BooleanField(
        default=False, verbose_name="accepté CGU",
        help_text="Les Conditions Générales d'Utilisation ont-elles été acceptées ?")

    objects = UserProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "Profile Utilisateur"
        verbose_name_plural = "Profiles Utilisateurs"

    @property
    def is_inspector(self):
        return self.profile_type == self.INSPECTOR

    @property
    def is_audited(self):
        return self.profile_type == self.AUDITED

    @property
    def questionnaires(self):
        """
        Returns the questionnaires belonging to the user.
        """
        Questionnaire = apps.get_model('control.Questionnaire')
        user_controls = self.controls.active()
        user_questionnaires = Questionnaire.objects.filter(control__in=user_controls)
        if self.is_audited:
            user_questionnaires = user_questionnaires.filter(is_draft=False)
        return user_questionnaires

    def __str__(self):
        return str(self.user)
