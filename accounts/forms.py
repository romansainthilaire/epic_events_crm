from django import forms

from accounts.models import User
from events.models import Client, Event


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.TextInput(attrs={"placeholder": ""})
        )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": ""})
        )


# --------------------  ↓  Forms used for admin site  ↓  --------------------


class ClientAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ClientAdminForm, self).__init__(*args, **kwargs)
        self.fields["sales_contact"].queryset = User.objects.filter(groups__name="vente")

    class Meta:
        model = Client
        fields = "__all__"


class EventAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventAdminForm, self).__init__(*args, **kwargs)
        self.fields["support_contact"].queryset = User.objects.filter(groups__name="support")

    class Meta:
        model = Event
        fields = ["contract", "support_contact"]
