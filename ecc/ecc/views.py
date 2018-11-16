from django.views.generic import TemplateView


login = TemplateView.as_view(template_name='ecc/login.html')
questionnaire_detail = TemplateView.as_view(template_name='ecc/questionnaire_detail.html')
questionnaire_list = TemplateView.as_view(template_name='ecc/questionnaire_list.html')
question_detail = TemplateView.as_view(template_name='ecc/question_detail.html')
