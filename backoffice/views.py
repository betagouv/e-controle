from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url


class AdminLoginView(LoginView):
    """
    A custom login view to the admin section.
    We don't use the default admin login view because it uses
    "?next=" redirections which are not safe.
    """
    template_name = 'admin/login.html'

    def get_success_url(self):
        """
        We override that default behaviour beacause we don't want next URL redirection.
        """
        return resolve_url('admin:index')
