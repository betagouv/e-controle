from django.views.generic import TemplateView


login = TemplateView.as_view(template_name='ecc/login.html')
cgu = TemplateView.as_view(template_name='ecc/cgu.html')
