from django import forms


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.TextInput(attrs={"placeholder": ""})
        )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": ""})
        )
