from django.db import models

class Media(models.Model):
    nom =  models.CharField(max_length=150)
    date_emprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.CharField(max_length=150)

    def emprunter(self, emprunteur):
        #Méthode pour emprunter un média
        if self.disponible:
            self.disponible = False
            self.emprunteur = emprunteur
            self.date_emprunt = models.DateField(auto_now=True)  # Met à jour la date d'emprunt
            self.save()
            print(f"{self.nom} a été emprunté par {emprunteur}.")
        else:
            print(f"{self.nom} n'est pas disponible pour l'emprunt.")

    def rendre(self):
        #Méthode pour rendre un média
        if not self.disponible:
            print(f"{self.nom} a été rendu par {self.emprunteur}.")
            self.disponible = True
            self.emprunteur = None
            self.date_emprunt = None
            self.save()
        else:
            print(f"{self.nom} est déjà disponible.")

    def __str__(self):
        return self.nom
    
class Livre(Media):
    auteur = models.CharField(max_length=150)

    def __str__(self):
        return f"Livre: {self.nom}, Auteur: {self.auteur}"


class Dvd(Media):
    realisateur= models.CharField(max_length=150)

    def __str__(self):
        return f"Dvd: {self.nom}, Réalisateur: {self.realisateur}"

class Cd(Media):
    interprete= models.CharField(max_length=150)

    def __str__(self):
        return f"Cd: {self.nom}, Interprete: {self.interprete}"
