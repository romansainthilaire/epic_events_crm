from django.contrib import admin

from events.models import Client, Contract, Event
from events.forms import ClientAdminForm, ContractAdminForm, EventAdminForm


class ClientAdmin(admin.ModelAdmin):

    form = ClientAdminForm
    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]
    search_fields = ["first_name", "last_name", "company_name"]


class ContractAdmin(admin.ModelAdmin):

    form = ContractAdminForm
    list_display = ["title", "amount", "client", "sales_contact", "signed"]
    list_filter = ["signed"]
    search_fields = ["title", "client"]


class EventAdmin(admin.ModelAdmin):

    form = EventAdminForm
    list_display = ["contract", "support_contact", "event_date", "attendees", "customer_satisfaction", "closed"]
    list_filter = ["closed"]
    search_fields = ["contract"]


admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
