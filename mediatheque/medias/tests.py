from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from .models import Media, Livre, Dvd, Cd, Emprunt
from mediatheque.models import Membre
from django.core.exceptions import ValidationError

class MediaTestCase(TestCase):
    def setUp(self):
        """Prépare les objets pour les tests"""
        self.membre = Membre.objects.create(nom="Charly")
        self.livre = Livre.objects.create(nom="Livre20", auteur="Author20", disponible=True)
        self.dvd = Dvd.objects.create(nom="DVD20", realisateur="Real20", disponible=True)
        self.cd = Cd.objects.create(nom="CD20", interprete="Interprete20", disponible=True)
        self.membre.save()
        self.livre.save()
        self.dvd.save()
        self.cd.save()

    def test_creation_media(self):
        """Test de la création d'un média"""
        media = Media.objects.create(nom="Test Media")
        self.assertEqual(media.nom, "Test Media")

    def test_emprunt_succes(self):
        """Test de l'emprunt d'un média avec succès"""
        result = Media.emprunter(self.livre.id, self.membre.id)
        self.livre.refresh_from_db()
        self.assertFalse(self.livre.disponible)
        self.assertIn("emprunté avec succès", result)

    def test_emprunt_deja_emprunte(self):
        """Test d'emprunt d'un média déjà emprunté"""
        Media.emprunter(self.livre.id, self.membre.id)
        result = Media.emprunter(self.livre.id, self.membre.id)
        self.assertIn("Ce média est déjà emprunté", result)
        
    def test_restitution_succes(self):
        """Test de la restitution d'un média"""
        Media.emprunter(self.livre.id, self.membre.id)
        result = Media.restituer(self.livre.id)
        self.livre.refresh_from_db()
        self.assertTrue(self.livre.disponible)
        self.assertIn("retourné avec succès", result)

    def test_get_type(self):
        """Test de la reconnaissance du type de média"""
        self.assertEqual(self.livre.get_type(), "Livre")
        self.assertEqual(self.dvd.get_type(), "DVD")
        self.assertEqual(self.cd.get_type(), "CD")

    def test_emprunt_str(self):
        """Test de la représentation en chaîne de caractères d'un emprunt"""
        emprunt = Emprunt.objects.create(media=self.livre, membre=self.membre)
        self.assertEqual(str(emprunt), f"Livre20 emprunté par Charly")

def test_membre_peut_emprunter(self):
    """Test de la limite d'emprunt à 3 médias"""
    # Créer 3 emprunts actifs
    for _ in range(3):
        Emprunt.objects.create(
            media=self.livre,
            membre=self.membre,
            date_emprunt=timezone.now()
        )

    # Vérifier qu'on ne peut pas en emprunter un 4ème
    with self.assertRaises(ValidationError) as context:
        Emprunt.membre_peut_emprunter(self.membre)

    self.assertEqual(
        str(context.exception),
        "{'__all__': ['Vous ne pouvez pas emprunter plus de 3 médias simultanément.']}"
    )