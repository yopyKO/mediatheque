from django import forms
from .models import Membre

class CreationMembreForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['nom', 'prenom']