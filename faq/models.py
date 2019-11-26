from django.db import models

from ckeditor.fields import RichTextField
from ordered_model.models import OrderedModel
from softdelete.models import SoftDeleteModel


class FAQItem(OrderedModel, SoftDeleteModel):
    title = models.CharField("title", max_length=255)
    slug = models.SlugField("slug", max_length=255)
    description = RichTextField("description", blank=True)

    class Meta:
        ordering = ('order',)
        verbose_name = "Item de F.A.Q"
        verbose_name_plural = "Items de F.A.Q"

    def __str__(self):
        return self.title
