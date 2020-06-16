from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'profile_type', 'send_files_report')
    list_filter = ('profile_type', 'controls')
    raw_id_fields = ('user',)
    filter_horizontal = ('controls',)
    search_fields = ('user__username',)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Utilisateurs'
    filter_horizontal = ('controls',)


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_staff',)
    list_filter = ('profile__profile_type', 'profile__controls')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
