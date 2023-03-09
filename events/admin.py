import datetime

from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib import messages

from events.models import Client, Contract, Event
from events.forms import ClientAdminForm, ContractAdminForm, EventAdminForm


# --------------------  ↓  Admin site for staff users with "vente" group  ↓  --------------------


class VenteAdminSite(AdminSite):

    site_header = "Epic Event Administration"
    site_title = "Epic Event"
    index_title = "Site d'administration - Vente"


class VenteClientAdmin(ModelAdmin):

    form = ClientAdminForm
    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]
    search_fields = ["first_name", "last_name", "company_name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(sales_contact=request.user)

    def save_model(self, request, obj, form, change):
        obj.sales_contact = request.user
        super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


class VenteContractAdmin(ModelAdmin):

    form = ContractAdminForm
    list_display = ["reference", "title", "amount", "payment_due_date", "signed"]
    list_editable = ["signed"]

    def reference(self, obj):
        return str(obj)

    def get_form(self, request, *args, **kwargs):
        form = super(VenteContractAdmin, self).get_form(request, *args, **kwargs)
        form.current_user = request.user
        return form

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(client__sales_contact=request.user)

    def save_model(self, request, obj, form, change):
        if form.changed_data == ["signed"]:
            if obj.signed:
                obj.signed_by = request.user.first_name.capitalize() + " " + request.user.last_name.upper()
                obj.save()
                event = Event()
                event.contract = obj
                event.save()
                super().save_model(request, obj, form, change)
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Il est impossible de retirer la signature d'un contrat.")
        elif obj.signed:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Un contrat signé ne peut pas être modifié.")
        else:
            payment_due_date = datetime.datetime.now().date() + datetime.timedelta(60)
            obj.payment_due_date = payment_due_date
            obj.save()

    def delete_model(self, request, obj):
        if obj.signed:
            messages.set_level(request, messages.ERROR)
            messages.error(request, "Un contrat signé ne peut pas être supprimé")
        else:
            return super().delete_model(request, obj)


class VenteEventAdmin(ModelAdmin):

    list_display = ["contract", "support_contact", "date", "attendees", "customer_satisfaction"]
    search_fields = ["contract"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


vente_admin_site = VenteAdminSite(name="admin-vente")
vente_admin_site.register(Client, VenteClientAdmin)
vente_admin_site.register(Contract, VenteContractAdmin)
vente_admin_site.register(Event, VenteEventAdmin)


# --------------------  ↓  Admin site for staff users with "support" group  ↓  --------------------


class SupportAdminSite(AdminSite):

    site_header = "Epic Event Administration"
    site_title = "Epic Event"
    index_title = "Site d'administration - Support"


class SupportClientAdmin(ModelAdmin):

    list_display = ["email", "first_name", "last_name", "company_name", "sales_contact"]
    search_fields = ["first_name", "last_name", "company_name"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        events = Event.objects.filter(support_contact=request.user)
        contracts = Contract.objects.filter(event__in=events)
        return queryset.filter(contracts__in=contracts).distinct()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SupportContractAdmin(ModelAdmin):

    list_display = ["reference", "title", "amount", "payment_due_date", "signed"]
    list_editable = ["signed"]

    def reference(self, obj):
        return str(obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        events = Event.objects.filter(support_contact=request.user)
        return queryset.filter(event__in=events)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SupportEventAdmin(ModelAdmin):

    form = EventAdminForm
    list_display = ["contract", "support_contact", "date", "attendees", "customer_satisfaction"]
    search_fields = ["contract"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(support_contact=request.user)

    def save_model(self, request, obj, form, change):
        date = obj.date
        contract = Contract.objects.filter(event=obj).first()
        if date < contract.date_updated.date():
            messages.set_level(request, messages.ERROR)
            messages.error(request, (
                "L'évènement ne peut pas avoir eu lieu avant la date de signature du contrat (" +
                contract.date_updated.date().strftime("%d/%m/%y") + ")."
            ))
        elif date > datetime.date.today():
            messages.set_level(request, messages.ERROR)
            messages.error(request, (
                "Vous ne pouvez pas rédiger un compte rendu pour un évènement qui n'a pas encore eu lieu."
            ))
        else:
            obj.save()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


support_admin_site = SupportAdminSite(name="admin-support")
support_admin_site.register(Client, SupportClientAdmin)
support_admin_site.register(Contract, SupportContractAdmin)
support_admin_site.register(Event, SupportEventAdmin)
