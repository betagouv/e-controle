from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from .models import Control, Questionnaire, Theme, Question, QuestionFile, ResponseFile
from .questionnaire_duplicate import QuestionnaireDuplicateMixin


class QuestionnaireInline(OrderedTabularInline):
    model = Questionnaire
    fields = ('title', 'description', 'uploaded_file', 'generated_file', 'end_date', 'move_up_down_links', 'order')
    readonly_fields = ('move_up_down_links',)
    extra = 1


@admin.register(Control)
class ControlAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('title', 'depositing_organization', 'reference_code')
    search_fields = (
        'title', 'reference_code,' 'questionnaires__title', 'questionnaires__description')
    inlines = (QuestionnaireInline, )


@admin.register(Questionnaire)
class QuestionnaireAdmin(QuestionnaireDuplicateMixin, OrderedModelAdmin):
    save_as = True
    list_display = ('numbering', 'title', 'sent_date', 'end_date', 'control', 'order')
    list_editable = ('order', 'control')
    readonly_fields = ('order',)
    search_fields = ('title', 'description')
    list_filter = ('control',)


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
class QuestionAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('more_details', 'numbering', 'description', 'theme', 'move_up_down_links')
    list_editable = ('description', 'theme')
    raw_id_fields = ('theme',)
    list_filter = ('theme', 'theme__questionnaire', 'theme__questionnaire__control')
    search_fields = ('description',)
    inlines = (QuestionFileInline,)

    def more_details(self, instance):
        return 'détails...'
    more_details.short_description = 'détails'


@admin.register(ResponseFile)
class ResponseFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'created', 'author')
    readonly_fields = ('question', 'file', 'author')
    date_hierarchy = 'created'
    list_filter = (
        'question__theme__questionnaire__control', 'question__theme__questionnaire',
        'author', 'question__theme')
    search_fields = ('author', 'file')


@admin.register(QuestionFile)
class QuestionFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file')
    readonly_fields = ('question', 'file')
    list_filter = (
        'question__theme__questionnaire__control', 'question__theme__questionnaire',
        'question__theme')
    search_fields = ('file',)
