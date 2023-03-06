import datetime

from django import forms
from django.core.exceptions import ValidationError

from events.models import Client, Contract, Event


class ClientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = ""
        self.fields["last_name"].widget.attrs["placeholder"] = ""
        self.fields["email"].widget.attrs["placeholder"] = ""
        self.fields["phone"].widget.attrs["placeholder"] = ""
        self.fields["mobile"].widget.attrs["placeholder"] = ""
        self.fields["company_name"].widget.attrs["placeholder"] = ""

    class Meta:
        model = Client
        exclude = ["sales_contact"]
        labels = {
            "first_name": "Prénom",
            "last_name": "Nom",
            "email": "Adresse e-mail",
            "phone": "Téléphone fixe",
            "mobile": "Téléphone mobile",
            "company_name": "Entreprise",
            }


class ContractForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = ""
        self.fields["content"].widget.attrs["placeholder"] = ""
        self.fields["amount"].widget.attrs["placeholder"] = ""

    class Meta:
        model = Contract
        exclude = ["client", "payment_due_date", "signed", "signed_by"]
        labels = {
            "title": "Titre",
            "content": "Termes et conditions",
            "amount": "Montant en euros (≥ 1000 euros)",
            }
        widgets = {
          "content": forms.Textarea(attrs={"rows": 15}),
        }


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["event_date"].widget.attrs["placeholder"] = "jj/mm/aaaa"
        self.fields["attendees"].widget.attrs["placeholder"] = ""
        self.fields["event_retrospective"].widget.attrs["placeholder"] = (
            "Lister ici :" + "\n"
            "\t- Les évènements marquants" + "\n"
            "\t- Les points positifs" + "\n"
            "\t- Les points négatifs" + "\n"
            "\t- Les axes d'amélioration"
            )

    class Meta:
        model = Event
        exclude = ["contract", "support_contact"]
        labels = {
            "event_date": "Date de l'évènement",
            "attendees": "Nombre de participants",
            "event_retrospective": "Retour d'expérience",
            "customer_satisfaction": "Satisfaction client (note sur 5)",
            }

    def clean_event_date(self, *args, **kwargs):
        event_date = self.cleaned_data["event_date"]
        if event_date > datetime.date.today():
            raise ValidationError(
                "Vous ne pouvez pas rédiger un compte rendu pour un évènement qui n'a pas encore eu lieu."
                )
        return event_date


# --------------------  ↓  Forms used for admin site - users with "vente" group  ↓  --------------------


class ClientAdminForm(forms.ModelForm):

    class Meta:
        model = Client
        exclude = ["sales_contact"]


class ContractAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContractAdminForm, self).__init__(*args, **kwargs)
        self.fields["client"].queryset = Client.objects.filter(sales_contact=self.current_user)

    class Meta:
        model = Client
        exclude = ["signed", "signed_by"]
