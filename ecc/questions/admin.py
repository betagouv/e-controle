from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Questionnaire, Theme, Question


@admin.register(Questionnaire)
class QuestionnaireAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links')
    search_fields = ('title', 'description')


@admin.register(Theme)
class ThemeAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(OrderedModelAdmin):
    list_display = ('description', 'move_up_down_links')
    search_fields = ('description',)
