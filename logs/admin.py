from django.contrib import admin
from django_admin import ReadOnlyModelAdmin

from actstream.models import Action, Follow


admin.site.unregister(Action)
admin.site.unregister(Follow)


@admin.register(Action)
class ActionAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = (
        '__str__', 'actor', 'verb', 'target', 'target_content_type', 'action_object',
        'action_object_content_type', 'timestamp')
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

    def has_delete_permission(self, request, obj=None):
        return True
