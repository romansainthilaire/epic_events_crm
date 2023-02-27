from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class LoginForm(forms.Form):

    email = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.TextInput(attrs={"placeholder": ""})
        )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": ""})
        )
