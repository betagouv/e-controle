from django.conf import settings
from django.db import models

from annoying.fields import AutoOneToOneField

from .managers import UserProfileQuerySet


class UserProfile(models.Model):
    PROFILE_TYPE = (
        ('audited', 'Organisme Contrôlé'),
        ('inspector', 'Contrôleur'),
    )
    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
        related_name='profile')
    profile_type = models.CharField(max_length=255, choices=PROFILE_TYPE)
    controls = models.ManyToManyField(
        to='control.Control', verbose_name='controles', related_name='user_profiles', blank=True)
    organization = models.CharField("Organisme", max_length=255, blank=True)
    send_files_report = models.BooleanField(
        verbose_name="Envoie Rapport de Fichiers", default=False,
        help_text="Envoyer par email le rapport des fichiers uplodés ?")

    objects = UserProfileQuerySet.as_manager()

    class Meta:
        verbose_name = "Profile Utilisateur"
        verbose_name_plural = "Profiles Utilisateurs"

    @property
    def is_inspector(self):
        return self.profile_type == 'inspector'

    @property
    def is_audited(self):
        return self.profile_type == 'audited'

    def __str__(self):
        return str(self.user)
