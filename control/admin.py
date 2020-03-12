from django_admin import ReadOnlyModelAdmin
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, RedirectView
from django.views.generic.detail import SingleObjectMixin


from ordered_model.admin import OrderedModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from utils.soft_delete import SoftDeletedAdmin, IsActiveFilter

from .models import Control, Questionnaire, Theme, Question, QuestionFile, ResponseFile
from .questionnaire_duplicate import QuestionnaireDuplicateMixin
from user_profiles.models import UserProfile


class ParentLinksMixin(object):
    def link_to_question(self, obj):
        question = None
        if hasattr(obj, 'question'):
            question = obj.question
        url = reverse("admin:control_question_change", args=[question.id])
        return mark_safe(f'<a href="{url}">{question}</a>')
    link_to_question.short_description = 'Question'

    def link_to_theme(self, obj):
        theme = None
        if hasattr(obj, 'theme'):
            theme = obj.theme
        if hasattr(obj, 'question'):
            theme = obj.question.theme
        url = reverse("admin:control_theme_change", args=[theme.id])
        return mark_safe(f'<a href="{url}">{theme}</a>')
    link_to_theme.short_description = 'Theme'

    def link_to_questionnaire(self, obj):
        questionnaire = None
        if hasattr(obj, 'questionnaire'):
            questionnaire = obj.questionnaire
        elif hasattr(obj, 'theme'):
            questionnaire = obj.theme.questionnaire
        elif hasattr(obj, 'question'):
            questionnaire = obj.question.theme.questionnaire

        url = reverse("admin:control_questionnaire_change", args=[questionnaire.id])
        return mark_safe(f'<a href="{url}">{questionnaire}</a>')
    link_to_questionnaire.short_description = 'Questionnaire'

    def link_to_control(self, obj):
        control = None
        if hasattr(obj, 'control'):
            control = obj.control
        elif hasattr(obj, 'questionnaire'):
            control = obj.questionnaire.control
        elif hasattr(obj, 'theme'):
            control = obj.theme.questionnaire.control
        elif hasattr(obj, 'question'):
            control = obj.question.theme.questionnaire.control

        url = reverse("admin:control_control_change", args=[control.id])
        return mark_safe(f'<a href="{url}">{control}</a>')
    link_to_control.short_description = 'Control'


class QuestionnaireInline(OrderedTabularInline):
    model = Questionnaire
    fields = (
        'id', 'title', 'description', 'uploaded_file', 'generated_file', 'end_date',
        'order', 'move_up_down_links')
    readonly_fields = ('id', 'move_up_down_links',)
    extra = 1


class UserProfileInline(admin.TabularInline):
    model = UserProfile.controls.through
    verbose_name_plural = 'Profils Utilisateurs'
    extra = 1
    fields = ('userprofile',)
    raw_id_fields = ('userprofile',)


@admin.register(Control)
class ControlAdmin(SoftDeletedAdmin, OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('id', 'title', 'depositing_organization', 'reference_code')
    search_fields = (
        'title', 'reference_code', 'questionnaires__title', 'questionnaires__description')
    list_filter = (IsActiveFilter,)
    inlines = (QuestionnaireInline, UserProfileInline, )


class ThemeInline(OrderedTabularInline):
    model = Theme
    fields = (
        'id', 'title', 'order', 'move_up_down_links')
    readonly_fields = ('id', 'order', 'move_up_down_links')
    extra = 1


@admin.register(Questionnaire)
class QuestionnaireAdmin(QuestionnaireDuplicateMixin, OrderedInlineModelAdminMixin, OrderedModelAdmin, ParentLinksMixin):
    save_as = True
    list_display = (
        'id', 'numbering', 'title', 'link_to_control', 'is_draft', 'editor',
        'sent_date', 'end_date')
    list_editable = ('order',)
    readonly_fields = ('order',)
    search_fields = ('title', 'description')
    list_filter = ('control', 'is_draft')
    raw_id_fields = ('editor', 'control')
    actions = ['megacontrol_admin_action']
    inlines = (ThemeInline, )


class QuestionInline(OrderedTabularInline):
    model = Question
    fields = ('id', 'description', 'order', 'move_up_down_links')
    readonly_fields = ('id', 'order', 'move_up_down_links')


@admin.register(Theme)
class ThemeAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin, ParentLinksMixin):
    list_display = ('id', 'numbering', 'title', 'link_to_questionnaire', 'link_to_control')
    search_fields = ('title',)
    list_filter = ('questionnaire__control', 'questionnaire',)
    fields = (
        'id', 'title', 'questionnaire', 'link_to_control')
    readonly_fields = ('id', 'link_to_control')
    inlines = (QuestionInline,)


class QuestionFileInline(OrderedTabularInline):
    model = QuestionFile
    max_num = 4
    fields = ('file', 'order', 'move_up_down_links')
    readonly_fields = ('order', 'move_up_down_links')


@admin.register(Question)
class QuestionAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin, ParentLinksMixin):
    list_display = ('id', 'numbering', 'description', 'link_to_theme', 'link_to_questionnaire',
        'link_to_control')
    fields = (
        'id', 'description', 'theme', 'link_to_questionnaire', 'link_to_control')
    readonly_fields = ('id', 'link_to_questionnaire', 'link_to_control')
    raw_id_fields = ('theme',)
    list_filter = ('theme', 'theme__questionnaire', 'theme__questionnaire__control')
    search_fields = ('description',)
    inlines = (QuestionFileInline,)


@admin.register(ResponseFile)
class ResponseFileAdmin(ReadOnlyModelAdmin, admin.ModelAdmin, ParentLinksMixin):
    list_display = (
        'id', 'file_name', 'link_to_question', 'link_to_theme', 'link_to_questionnaire',
        'link_to_control', 'created', 'author', 'is_deleted')
    list_display_links = ('id',)
    date_hierarchy = 'created'
    list_filter = (
        'question__theme__questionnaire__control', 'question__theme__questionnaire',
        'author', 'question__theme')
    fields = (
        'id', 'author', 'file_name', 'link_to_question', 'link_to_questionnaire', 'link_to_control',
        'created', 'modified', 'is_deleted')
    readonly_fields = ('file_name', 'link_to_question', 'link_to_questionnaire', 'link_to_control')
    search_fields = (
        'file', 'question__description', 'author__first_name', 'author__last_name',
        'author__username')


@admin.register(QuestionFile)
class QuestionFileAdmin(admin.ModelAdmin, ParentLinksMixin):
    list_display = (
        'id', 'file', 'link_to_question', 'link_to_theme', 'link_to_questionnaire',
        'link_to_control')
    list_display_links = ('id',)
    list_filter = (
        'question__theme__questionnaire__control', 'question__theme__questionnaire',
        'question__theme')
    fields = (
        'id', 'file', 'question', 'order', 'link_to_questionnaire', 'link_to_control')
    readonly_fields = (
        'id', 'order', 'link_to_questionnaire', 'link_to_control')
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
