from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .models import FAQItem


@admin.register(FAQItem)
class FAQItemAdmin(OrderedModelAdmin):
    list_display = ('title',  'slug', 'order', 'move_up_down_links')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('order', 'move_up_down_links')
    search_fields = ('title', 'description')
    ordering = ('order',)
