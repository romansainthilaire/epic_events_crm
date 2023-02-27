from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):

    # UserAdmin is used to hash passwords when creating users with the admin site
    # https://stackoverflow.com/questions/32851901/django-admin-not-hashing-users-password

    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "is_admin", "team"]
    search_fields = ["email"]
    ordering = []
    list_filter = ["groups__name", "is_active"]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    # fields accessed when creating a user
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": ["first_name", "last_name", "email", "password1", "password2", "is_active", "is_staff", "groups"]
            }
         )
    ]

    # fields accessed when updating a user
    fieldsets = [
        (None, {"fields": ["first_name", "last_name", "email", "password"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "groups"]}),
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_admin:
            return queryset  # admin users can access all users
        else:
            return queryset.filter(is_admin=False)  # staff users can access all users except admin users

    def team(self, obj):
        """
        Return groups separated by comma.
        Return empty string if no group.
        """
        return ", ".join([g.name for g in obj.groups.all()]) if obj.groups.count() else ""


admin.site.register(User, CustomUserAdmin)
