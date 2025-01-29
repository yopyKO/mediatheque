from django import forms
from medias.models import Livre, Dvd, Cd

class CreationLivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['nom', 'auteur']

class CreationDvdForm(forms.ModelForm):
    class Meta:
        model = Dvd
        fields = ['nom', 'realisateur']

class CreationCdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = ['nom', 'interprete']