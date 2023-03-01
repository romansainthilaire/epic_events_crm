from django import forms

from accounts.models import User
from events.models import Client, Contract, Event


class ClientAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientAdminForm, self).__init__(*args, **kwargs)
        self.fields["sales_contact"].queryset = User.objects.filter(groups__name="vente")

    class Meta:
        model = Client
        fields = "__all__"


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
        exclude = ["client", "payment_due_date", "signed"]
        labels = {
            "title": "Titre",
            "content": "Termes et conditions",
            "amount": "Montant en euros (≥ 1000 euros)",
            }
        widgets = {
          "content": forms.Textarea(attrs={"rows": 15}),
        }


class EventAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields["support_contact"].queryset = User.objects.filter(groups__name="support")

    class Meta:
        model = Event
        fields = ["contract", "support_contact"]


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = ["contract", "support_contact"]
