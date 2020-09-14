from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url


class AdminLoginView(LoginView):
    """
    A custom login view to the admin section.
    We don't use the default admin login view because it uses
    "?next=" redirections which are not safe.
    """
    template_name = 'admin/login.html'  # Let's use the template shipped with Django

    def get_success_url(self):
        return resolve_url('admin:index')
