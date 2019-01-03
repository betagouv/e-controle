from django.conf import settings
from django.db import models

from annoying.fields import AutoOneToOneField


class UserProfile(models.Model):
    PROFILE_TYPE = (
        ('audited', 'Organisme Controlé'),
        ('inspector', 'Controleur'),
    )
    user = AutoOneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
        related_name='profile')
    profile_type = models.CharField(max_length=255, choices=PROFILE_TYPE)
    control = models.ForeignKey(
        to='control.Control', verbose_name='controle', related_name='user_profiles',
        null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.CharField("Organisme", max_length=255, blank=True)

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
