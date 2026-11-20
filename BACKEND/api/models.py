from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrateur'),
        ('USER', 'Utilisateur'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Categorie(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nom


class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    biographie = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Livre(models.Model):
    titre = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)
    description = models.TextField(blank=True)
    
   
    couverture = models.ImageField(upload_to='couvertures/', null=True, blank=True)
    
    
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE, related_name="livres")
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name="livres")
    
    quantite_stock = models.PositiveIntegerField(default=1)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    

    
class Emprunt(models.Model):
    STATUT_CHOICES = (
        ('EN_COURS', 'En cours'),
        ('RETOURNE', 'Retourné'),
        ('EN_RETARD', 'En retard'),
    )
    
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emprunts")
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name="emprunts")
    
    # Les dates
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prevue = models.DateField() # La date limite pour rendre le livre
    date_retour_effective = models.DateField(null=True, blank=True) # Rempli quand le livre est rendu
    
    
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='EN_COURS')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.livre.titre} ({self.statut})"