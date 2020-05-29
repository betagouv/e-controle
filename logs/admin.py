from django_admin import ReadOnlyModelAdmin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html


from actstream.models import Action, Follow


admin.site.unregister(Action)
admin.site.unregister(Follow)


def get_admin_url(obj):
    """
    Return the admin page URL for the given objet
    """
    content_type = ContentType.objects.get_for_model(obj.__class__)
    app_label = content_type.app_label
    model = content_type.model
    return reverse(f"admin:{app_label}_{model}_change", args=(obj.pk,))


def get_object_display_line(obj):
    """
    For the given object, return a display line with HTML link to the admin page.
    """
    if not obj:
        return '-'
    url = get_admin_url(obj)
    return format_html(
        '<a href="{}">{}</a>',
        url,
        obj
    )


def action_display(obj):
    return get_object_display_line(obj)


def actor_display(obj):
    return get_object_display_line(obj.actor)


def target_display(obj):
    return get_object_display_line(obj.target)


def action_object_display(obj):
    return get_object_display_line(obj.action_object)


action_display.short_description = 'action'
actor_display.short_description = 'actor'
target_display.short_description = 'target'
action_object_display.short_description = 'action_object'


@admin.register(Action)
class ActionAdmin(ReadOnlyModelAdmin, admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = (
        'id', action_display, actor_display, 'verb', target_display, 'target_content_type',
        action_object_display, 'action_object_content_type', 'timestamp')
    list_filter = ('timestamp', 'verb')
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
