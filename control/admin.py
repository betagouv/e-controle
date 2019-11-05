from django_admin import ReadOnlyModelAdmin
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, RedirectView
from django.views.generic.detail import SingleObjectMixin


from ordered_model.admin import OrderedModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from .models import Control, Questionnaire, Theme, Question, QuestionFile, ResponseFile
from .questionnaire_duplicate import QuestionnaireDuplicateMixin


class AdminHelpers(object):

    def more_details(self, instance):
        return 'détails...'
    more_details.short_description = 'détails'


class QuestionnaireInline(OrderedTabularInline):
    model = Questionnaire
    fields = (
        'title', 'description', 'uploaded_file', 'generated_file', 'end_date',
        'move_up_down_links', 'order')
    readonly_fields = ('move_up_down_links',)
    extra = 1


@admin.register(Control)
class ControlAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('title', 'depositing_organization', 'reference_code')
    search_fields = (
        'title', 'reference_code', 'questionnaires__title', 'questionnaires__description')
    inlines = (QuestionnaireInline, )


@admin.register(Questionnaire)
class QuestionnaireAdmin(QuestionnaireDuplicateMixin, OrderedModelAdmin):
    save_as = True
    list_display = (
        'id', 'title', 'control', 'numbering', 'order', 'is_draft', 'editor',
        'sent_date', 'end_date')
    list_editable = ('order', 'control')
    readonly_fields = ('order',)
    search_fields = ('title', 'description')
    list_filter = ('control', 'is_draft')
    raw_id_fields = ('editor',)
    actions = ['megacontrol_admin_action']


class QuestionInline(OrderedTabularInline):
    model = Question
    fields = ('description', 'order', 'move_up_down_links')
    readonly_fields = ('order', 'move_up_down_links')


@admin.register(Theme)
class ThemeAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('numbering', 'title', 'questionnaire', 'move_up_down_links')
    list_editable = ('title', 'questionnaire')
    search_fields = ('title',)
    list_filter = ('questionnaire__control', 'questionnaire',)
    inlines = (QuestionInline,)


class QuestionFileInline(OrderedTabularInline):
    model = QuestionFile
    max_num = 4
    fields = ('file', 'order', 'move_up_down_links')
    readonly_fields = ('order', 'move_up_down_links')


@admin.register(Question)
class QuestionAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin, AdminHelpers):
    list_display = ('more_details', 'numbering', 'description', 'theme', 'move_up_down_links')
    list_editable = ('description', 'theme')
    raw_id_fields = ('theme',)
    list_filter = ('theme', 'theme__questionnaire', 'theme__questionnaire__control')
    search_fields = ('description',)
    inlines = (QuestionFileInline,)


@admin.register(ResponseFile)
class ResponseFileAdmin(ReadOnlyModelAdmin, admin.ModelAdmin, AdminHelpers):
    list_display = (
        'more_details', 'id', 'file_name', 'question_display', 'questionnaire_display',
        'control_display', 'created', 'author', 'is_deleted')
    list_display_links = ('more_details', 'id')
    date_hierarchy = 'created'
    list_filter = (
        'question__theme__questionnaire__control', 'question__theme__questionnaire',
        'author', 'question__theme')
    fields = (
        'id', 'author', 'file_name', 'question_display', 'questionnaire_display', 'control_display',
        'created', 'modified', 'is_deleted')
    readonly_fields = ('file_name', 'question_display', 'questionnaire_display', 'control_display')
    search_fields = (
        'file', 'question__description', 'author__first_name', 'author__last_name',
        'author__username')


@admin.register(QuestionFile)
class QuestionFileAdmin(admin.ModelAdmin, AdminHelpers):
    list_display = (
        'more_details', 'id', 'file', 'question_display', 'questionnaire_display',
        'control_display')
    list_display_links = ('more_details', 'id')
    list_filter = (
        'question__theme__questionnaire__control', 'question__theme__questionnaire',
        'question__theme')
    fields = (
        'id', 'file', 'question', 'question_display', 'questionnaire_display',
        'control_display', 'order')
    readonly_fields = (
        'id', 'question_display', 'questionnaire_display', 'control_display', 'order')
    search_fields = ('file', 'question__description')
    raw_id_fields = ('question',)


@method_decorator(staff_member_required, name='dispatch')
class MegacontrolConfirm(QuestionnaireDuplicateMixin, DetailView):
    template_name = "ecc/megacontrol_confirm.html"
    context_object_name = 'questionnaire'

    def get_queryset(self):
        return Questionnaire.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['controls_to_copy_to'] = self.get_controls_to_copy_to(self.object)
        return context


@method_decorator(staff_member_required, name='dispatch')
class Megacontrol(LoginRequiredMixin, QuestionnaireDuplicateMixin, SingleObjectMixin, RedirectView):
    url = '/admin/control/questionnaire/'
    model = Questionnaire

    def get_queryset(self):
        return Questionnaire.objects.all()

    def get(self, *args, **kwargs):
        questionnaire = self.get_object()
        created_questionnaires = self.do_megacontrol(questionnaire)

        message = (
            f'Vous avez créé les <b>{ len(created_questionnaires) }</b> questionnaires suivants : <ul>')
        for created_questionnaire in created_questionnaires:
            message += f'<li>'
            message += f'  <a href="/admin/control/questionnaire/{created_questionnaire.id}/change/">'
            message += f'    <b> {created_questionnaire.id} : {created_questionnaire} </b>'
            message += f'  </a>'
            message += f'  dans l\'espace <b>{ created_questionnaire.control }</b>'
            message += f'</li>'
        message += '</ul>'
        messages.success(self.request, mark_safe(message))

        return super().get(*args, **kwargs)
