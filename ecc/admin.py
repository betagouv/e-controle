from django.contrib import admin
from django_admin import ReadOnlyModelAdmin

from magicauth.models import MagicToken


admin.site.unregister(MagicToken)


@admin.register(MagicToken)
class MagicTokenAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    list_display = ('user', 'created')
    list_display_links = None
    raw_id_fields = ('user',)
    date_hierarchy = ('created')
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    fieldsets = [
        (None, {'fields': ()})
    ]
