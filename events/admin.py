from django.contrib import admin

from events.models import Client, Event
from events.forms import ClientAdminForm, EventAdminForm


class ClientAdmin(admin.ModelAdmin):

    form = ClientAdminForm
    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]
    search_fields = ["first_name", "last_name", "company_name"]


class EventAdmin(admin.ModelAdmin):

    form = EventAdminForm
    list_display = ["contract", "support_contact", "event_date", "attendees", "customer_satisfaction", "closed"]
    list_filter = ["closed"]
    search_fields = ["contract"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Event, EventAdmin)
