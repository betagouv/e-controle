from django.db import models

from mptt.models import MPTTModel, TreeForeignKey
from ordered_model.models import OrderedModel


class Questionnaire(OrderedModel):
    title = models.CharField("titre", max_length=255)
    description = models.TextField("description", blank=True)

    class Meta:
        ordering = ('order',)
        verbose_name = "Questionnaire"
        verbose_name_plural = "Questionnaires"

    def __str__(self):
        return self.title


class Theme(MPTTModel):
    title = models.CharField("titre", max_length=255)
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
        'theme', verbose_name='theme', related_name='questions', on_delete=models.CASCADE)
    order_with_respect_to = 'theme'

    class Meta:
        ordering = ('theme', 'order')
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return self.description
