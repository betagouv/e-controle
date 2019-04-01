from django.db import models


class UserProfileQuerySet(models.query.QuerySet):

    def inspectors(self):
        return self.filter(profile_type='inspector')

    def audited(self):
        return self.filter(profile_type='audited')
