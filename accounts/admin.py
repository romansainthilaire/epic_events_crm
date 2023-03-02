from django.contrib import admin
from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User
from events.models import Client, Contract, Event
from events.forms import ClientAdminForm, EventAdminForm

# BaseUserAdmin is used to hash passwords when creating users with the admin site
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/


# ------------------------------ Admin site for admin users ------------------------------

admin.site.site_header = "Epic Event Administration"
admin.site.site_title = "Epic Event"


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

    def team(self, obj):
        """
        Return groups separated by comma.
        Return empty string if no group.
        """
        return ", ".join([g.name for g in obj.groups.all()]) if obj.groups.count() else ""


class ClientAdmin(ModelAdmin):

    form = ClientAdminForm
    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]
    search_fields = ["first_name", "last_name", "company_name"]


class ContractAdmin(ModelAdmin):

    list_display = ["title", "amount", "payment_due_date", "signed"]


class EventAdmin(ModelAdmin):

    form = EventAdminForm
    list_display = ["contract", "support_contact", "event_date", "attendees", "customer_satisfaction"]
    search_fields = ["contract"]


admin.site.register(User, UserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)


# ------------------------------ Admin site for users with "gestion" group ------------------------------

class GestionAdminSite(AdminSite):

    site_header = "Epic Event Administration"
    site_title = "Epic Event"
    index_title = "Site d'administration - Gestion"


class GestionUserAdmin(UserAdmin):

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_admin=False)

    def has_delete_permission(self, request, obj=None):
        return False


class GestionClientAdmin(ClientAdmin):

    form = ClientAdminForm
    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]
    search_fields = ["first_name", "last_name", "company_name"]

    def has_delete_permission(self, request, obj=None):
        return False


class GestionEventAdmin(ClientAdmin):

    form = EventAdminForm
    list_display = ["contract", "support_contact", "event_date", "attendees", "customer_satisfaction"]
    search_fields = ["contract"]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


gestion_admin_site = GestionAdminSite(name="gestion-admin")
gestion_admin_site.register(User, GestionUserAdmin)
gestion_admin_site.register(Client, GestionClientAdmin)
gestion_admin_site.register(Event, GestionEventAdmin)
