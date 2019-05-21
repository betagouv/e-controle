from django.apps import AppConfig


class UserProfilesConfig(AppConfig):
    name = 'user_profiles'
    verbose_name = "Profiles Utilisateurs"

    def ready(self):
        import user_profiles.signals  # noqa
