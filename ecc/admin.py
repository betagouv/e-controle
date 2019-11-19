from django.contrib import admin
from django_admin import ReadOnlyModelAdmin

from actstream.models import Action, Follow
from magicauth.models import MagicToken


admin.site.unregister(Action)
admin.site.unregister(Follow)
admin.site.unregister(MagicToken)


@admin.register(Action)
class ActionAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('__str__', 'actor', 'verb', 'target', 'action_object', 'timestamp')
    list_filter = ('timestamp', 'verb',)
    fieldsets = (
        (None, {
            'fields': ('verb', 'timestamp', 'description')
        }),
        ('Actor', {
            'fields': ('actor', 'actor_content_type', 'actor_object_id'),
        }),
        ('Action', {
            'fields': ('action_object', 'action_object_content_type', 'action_object_object_id'),
        }),
        ('Target', {
            'fields': ('target', 'target_content_type', 'target_object_id'),
        }),
    )
    search_fields = ('verb', 'description', 'actor_object_id')
    readonly_fields = ('actor', 'action_object', 'target')


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
