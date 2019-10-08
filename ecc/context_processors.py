from django.conf import settings
from django.contrib.sites.models import Site


def debug(request):
    return {'debug': settings.DEBUG}


def current_site(request):
    return {'current_site': Site.objects.get_current()}
