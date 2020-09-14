from django.views.generic import TemplateView


class FAQ(TemplateView):
    template_name = "ecc/faq.html"
