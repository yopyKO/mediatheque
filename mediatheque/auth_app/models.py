from django.db import models

class Utilisateur(models.Model):
    nom = models.CharField(max_length=50)
    mot_de_passe = models.CharField(max_length=50)

class Livre(models.Model):
    nom = models.CharField(max_length=55)
    auteur = models.CharField(max_length=55)

    def __str__(self):
        return self.nom