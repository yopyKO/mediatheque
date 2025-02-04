from django import forms
from medias.models import Media, Livre, Dvd, Cd

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['nom']  # Champs communs à tous les médias

class CreationLivreForm(MediaForm):
    class Meta:
        model = Livre
        fields = MediaForm.Meta.fields + ['auteur']  # Ajout du champ spécifique au livre

class CreationDvdForm(forms.ModelForm):
    class Meta:
        model = Dvd
        fields = MediaForm.Meta.fields + ['realisateur'] # Ajout du champ spécifique au dvd

class CreationCdForm(forms.ModelForm):
    class Meta:
        model = Cd
        fields = MediaForm.Meta.fields + ['interprete'] # Ajout du champ spécifique au cd