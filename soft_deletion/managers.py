from django.db import models


class DeletableQuerySet(models.QuerySet):

    def active(self):
        return self.filter(deleted_at__isnull=True)
