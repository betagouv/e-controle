from django import template

from faq.models import FAQItem


register = template.Library()


@register.simple_tag
def get_faq_items():
    return FAQItem.objects.filter(deleted_at__isnull=True)
