from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login as django_login
from django.contrib.auth import logout
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View


User = get_user_model()


class DemoView(View):
    """
    This view allows to login with a demo user.
    The demo user that you'll impersonate should not have admin privileges.
    Also, this view is meant to work only on DEBUG mode.
    """

    def get(self, request):
        if not settings.DEBUG or not settings.ALLOW_DEMO_LOGIN:
            raise Http404
        logout(request)
        user = User.objects.filter(username=self.demo_username).first()
        is_not_admin = user and not user.is_staff and not user.is_superuser
        if is_not_admin:
            django_login(request, user)
            return HttpResponseRedirect(reverse('questionnaire-list'))
        return HttpResponseRedirect(reverse('login'))


class DemoInspectorView(DemoView):

    @property
    def demo_username(self):
        return settings.DEMO_INSPECTOR_USERNAME


class DemoAuditedView(DemoView):

    @property
    def demo_username(self):
        return settings.DEMO_AUDITED_USERNAME
