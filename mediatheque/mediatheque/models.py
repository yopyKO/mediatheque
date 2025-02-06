from django.db import models

class Jeu(models.Model):
    nom = models.CharField(max_length=55)

    def __str__(self):
        return self.nom
    
class Membre(models.Model):
    nom = models.CharField(max_length=55)
    prenom = models.CharField(max_length=55)

    def nombre_emprunts_actifs(self):
        from medias.models import Emprunt
        return Emprunt.objects.filter(membre=self, date_retour__isnull=True).count()
    
    def __str__(self):
        return f"Nom: {self.nom}, Prenom: {self.prenom}"