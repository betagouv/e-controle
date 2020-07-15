from django.contrib.auth.views import LoginView as BaseLoginView
from django.shortcuts import resolve_url


class LoginView(BaseLoginView):
    """
    A custom login view to the admin section.
    """
    template_name = 'admin/login.html'

    def get_success_url(self):
        """
        We override that default behaviour beacause we don't want next URL redirection.
        """
        return resolve_url('admin:index')
