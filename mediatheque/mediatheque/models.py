from datetime import date, timedelta
from django.db import models

class Jeu(models.Model):
    nom = models.CharField(max_length=55)

    def __str__(self):
        return self.nom
    
class Membre(models.Model):
    nom = models.CharField(max_length=55)
    prenom = models.CharField(max_length=55)

    def __str__(self):
        return f"Nom: {self.nom}, Prenom: {self.prenom}"