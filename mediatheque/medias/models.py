from django.db import models

class Medias():
    name =  models.fields.CharField(max_length=150)
    dateEmprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    emprunteur = models.fields.CharField(max_length=150)

    def __init__(self, name, dateEmprunt, disponible, emprunteur):
        self.name = name
        self.dateEmprunt = dateEmprunt
        self.disponible = disponible
        self.emprunteur = emprunteur

    def description(self):
        return f"{self.name} emprunté le, {self.dateEmprunt} - Disponible : {self.disponible} | Emprunteur : {self.emprunteur}"
    
class Livre(Medias):
    auteur = models.fields.CharField(max_length=150)

    def __init__(self, name, dateEmprunt, disponible, emprunteur, auteur):
        # Appel du constructeur de la classe parente
        super().__init__(name, dateEmprunt, disponible, emprunteur)
        self.auteur = auteur

    def description(self):
        base_description = super().description()  # Appelle la méthode description de Medias
        return f" - Auteur : {self.auteur} | {base_description}"

    def lecture(self):
        print("Livre de " + self.auteur) 

class Dvd(Medias):
    réalisateur= models.fields.CharField(max_length=150)

    def __init__(self, titre, réalisateur, dateEmprunt, disponible, emprunteur):
        self.titre = titre
        self.réalisateur = réalisateur
        self.dateEmprunt = dateEmprunt
        self.disponible = disponible
        self.emprunteur = emprunteur

    def description(self):
        return self.titre + " de " + self.réalisateur + ", emprunté le " + self.dateEmprunt + " par " + self.emprunteur
    
Dvd1 = Dvd('Interstellar', 'Chrisopher Nolan', '25/12/2024', 'non', 'George Dupont')

class Cd(Medias):
    interprete= models.fields.CharField(max_length=150)


    def __init__(self, titre, interprete, dateEmprunt, disponible, emprunteur):
        self.titre = titre
        self.interprete = interprete
        self.dateEmprunt = dateEmprunt
        self.disponible = disponible
        self.emprunteur = emprunteur

    def description(self):
        return self.titre + " de " + self.interprete + ", emprunté le " + self.dateEmprunt + " par " + self.emprunteur
