from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin
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
    list_display = ('title',)
    search_fields = ('title', 'questionnaires__title', 'questionnaires__description')
    inlines = (QuestionnaireInline, )


@admin.register(Theme)
class ThemeAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'title', 'questionnaire')
    list_editable = ('title', 'questionnaire')
    search_fields = ('title',)


class QuestionFileInline(OrderedTabularInline):
    model = QuestionFile
    max_num = 4
    fields = ('file', 'order', 'move_up_down_links',)
    readonly_fields = ('order', 'move_up_down_links',)


@admin.register(Question)
class QuestionAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    list_display = ('id', 'description', 'theme', 'move_up_down_links')
    list_editable = ('description', 'theme')
    list_filter = ('theme', 'theme__questionnaire', 'theme__questionnaire__control')
    search_fields = ('description',)
    inlines = (QuestionFileInline,)


@admin.register(ResponseFile)
class ResponseFileAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
