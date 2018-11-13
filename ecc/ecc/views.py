from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "ecc/home.html"


home = Home.as_view()
