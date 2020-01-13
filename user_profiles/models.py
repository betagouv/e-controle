from django.conf import settings
from django.db import models

from annoying.fields import AutoOneToOneField

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

    def __str__(self):
        return str(self.user)
