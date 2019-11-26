from django.contrib import admin


def soft_delete(modeladmin, request, queryset):
    for item in queryset:
        item.soft_delete()


def undelete(modeladmin, request, queryset):
    for item in queryset:
        item.undelete()


soft_delete.short_description = "Supprimer les éléments sélectionnés"
undelete.short_description = "Restaurer les éléments sélectionnés"


class IsDeletedFilter(admin.SimpleListFilter):
    title = 'deleted'
    parameter_name = 'deleted'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(deleted_at__isnull=False)
        elif value == 'no':
            return queryset.exclude(deleted_at__isnull=False)
        return queryset


class SoftDeletedAdmin(object):

    def is_deleted(self, instance):
        return instance.is_deleted()
    is_deleted.boolean = True
    is_deleted.short_description = "deleted"
    actions = [soft_delete, undelete]

    def get_list_filter(self, request):
        return super().get_list_filter(request) + (IsDeletedFilter,)

    def get_list_display(self, request):
        return super().get_list_display(request) + ('deleted_at', 'is_deleted')

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + ('deleted_at',)

    def has_delete_permission(self, request, obj=None):
        return False
