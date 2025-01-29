from django import forms
from django.contrib.auth.forms import UserCreationForm
from auth_app.models import Livre

# creating forms
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Saisir le mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        strip=False,
    )
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("password1", "password2")
