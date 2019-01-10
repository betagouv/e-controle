from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin
from ordered_model.admin import OrderedTabularInline, OrderedInlineModelAdminMixin

from .models import Control, Questionnaire, Theme, Question, QuestionFile, ResponseFile


class QuestionnaireInline(OrderedTabularInline):
    model = Questionnaire
    fields = ('title', 'description', 'end_date', 'move_up_down_links')
    readonly_fields = ('order', 'move_up_down_links')
    extra = 1


@admin.register(Control)
class ControlAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('title', 'reference_code')
    search_fields = (
        'title', 'reference_code,' 'questionnaires__title', 'questionnaires__description')
    inlines = (QuestionnaireInline, )


@admin.register(Questionnaire)
class QuestionnaireAdmin(OrderedModelAdmin):
    list_display = ('numbering', 'title', 'end_date', 'control')
    search_fields = ('title', 'description')
    list_filter = ('control',)


@admin.register(Theme)
class ThemeAdmin(OrderedModelAdmin):
    list_display = ('numbering', 'title', 'questionnaire', 'move_up_down_links')
    list_editable = ('title', 'questionnaire')
    search_fields = ('title',)
    list_filter = ('questionnaire',)


class QuestionFileInline(OrderedTabularInline):
    model = QuestionFile
    max_num = 4
    fields = ('file', 'order', 'move_up_down_links')
    readonly_fields = ('order', 'move_up_down_links')


@admin.register(Question)
class QuestionAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('more_details', 'numbering', 'description', 'theme', 'move_up_down_links')
    list_editable = ('description', 'theme')
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
