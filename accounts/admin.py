from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User
from events.models import Client, Contract, Event

# BaseUserAdmin is used to hash passwords when creating users with the admin site
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/


class UserAdmin(BaseUserAdmin):

    list_display = ["email", "first_name", "last_name", "is_active", "is_staff", "is_admin", "team"]
    list_filter = ["groups__name", "is_active"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = []

    # fields displayed when creating a user
    add_fieldsets = [
        ("Identifiants", {"fields": ["first_name", "last_name", "email", "password1", "password2"]}),
        ("Permissions", {"fields": ["is_active", "is_staff", "groups"]}),
    ]

    # fields displayed when updating a user
    fieldsets = [
        ("Identifiants", {"fields": ["first_name", "last_name", "email", "password"]}),
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


class ClientAdmin(admin.ModelAdmin):

    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]


class ContractAdmin(admin.ModelAdmin):

    list_display = ["title", "amount", "client", "sales_contact", "signed"]


class EventAdmin(admin.ModelAdmin):

    list_display = ["contract", "support_contact", "event_date", "attendees"]


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
