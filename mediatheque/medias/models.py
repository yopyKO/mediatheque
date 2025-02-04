from datetime import date, timedelta
from django.db import models
from mediatheque.models import Membre
from django.utils import timezone
from django.core.exceptions import ValidationError

class Media(models.Model):
    nom =  models.CharField(max_length=150)
    date_emprunt = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=True)
    membre = models.CharField(max_length=150)

    def emprunter(media_id, membre_id):
        try:
            media = Media.objects.get(id=media_id)
            membre = membre.objects.get(id=membre_id)

            if not media.disponible:
                raise ValidationError("Ce media est déjà emprunté.")

            # Création de l'emprunt
            emprunt = Emprunt.objects.create(
                media=media,
                membre=membre,
                date_emprunt=timezone.now(),
                date_retour=timezone.now() + timezone.timedelta(days=7) # 7 jours de durée d'emprunt max
            )

            # Marquer le média comme indisponible
            media.disponible = False
            media.save()

            return f"Média '{media.nom}' emprunté avec succès par {membre.nom} jusqu'au {emprunt.date_retour}."

        except Media.DoesNotExist:
            return "Média introuvable."
        except Membre.DoesNotExist:
            return "Emprunteur introuvable."
        except ValidationError as e:
            return str(e)

    def restituer(media_id):
        try:
            media = Media.objects.get(id=media_id)
            emprunt = Emprunt.objects.get(media=media, date_retour__gte=timezone.now())

            # Supprimer l'emprunt ou le marquer comme terminé
            emprunt.delete()

            # Rendre le média disponible
            media.disponible = True
            media.save()

            return f"Média '{media.nom}' retourné avec succès."
        
        except Media.DoesNotExist:
            return "Média introuvable."
        except Emprunt.DoesNotExist:
            return "Ce média n'était pas emprunté."
    
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

class Emprunt(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(default=date.today() + timedelta(days=7))  # Retour dans 7 jours

    def __str__(self):
        return f"{self.media.nom} emprunté par {self.membre.nom}"