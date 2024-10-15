from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User 
from datetime import datetime;
from ckeditor.fields import RichTextField


# 1
class Personnel(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="personnel_user")
    nom_prenom=models.CharField(max_length=100,blank=True, null=True)
    
    date_naissance =models.DateField(default=datetime.now,null=True)
    genre =models.CharField(max_length=100,null=True)
    role = models.CharField(max_length=50, null=True,choices=[('Choisisez','Choisisez'),('Chef', 'Chef'), ('Responsable', 'Responsable'),('Technicien','Technicien')])
    telephone =models.CharField(max_length=100,null=True)
    address=models.CharField(max_length=100, null = True)
    date_enre=models.DateField(default=datetime.now,null=True)


    def __str__(self):
        return self.nom_prenom if self.nom_prenom else "Nom non spécifié"


#2
class Financement(models.Model):
    nom_societe=models.CharField(max_length=100,null=True)
    date_debut=models.DateField(null=True)
    date_fin=models.DateField()

    def __str__(self):
        return self.nom_societe if self.nom_societe else "Nom non spécifié"
#3
class Projet(models.Model):
    nom_projet=models.CharField(max_length=100,null=True)
    responsable_projet=models.ForeignKey(Personnel,on_delete=models.CASCADE,null=True)
    finance_par=models.ForeignKey(Financement,on_delete=models.CASCADE,null=True)
    date_debut=models.DateField(null=True)
    date_fin=models.DateField()
    description_projet=models.CharField(max_length=100,null=True)
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')

    def __str__(self):
        return self.nom_projet if self.nom_projet else "Nom non spécifié"
# 4

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)  # Le champ timestamp pour enregistrer l'heure de l'action

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"


class Site(models.Model):
    nom_site=models.CharField(max_length=100,null=True)
    
    chef_d_equipe=models.ForeignKey(Personnel,on_delete=models.CASCADE,null=True)
    finance_par=models.ForeignKey(Financement,on_delete=models.CASCADE,null=True)
    lieu=models.CharField(max_length=100,null=True)
    date_debut=models.DateField(null=True)
    date_fin=models.DateField()

    def __str__(self):
        return self.nom_site if self.nom_site else "Nom non spécifié"

#5
class Rapport(models.Model):
    personnel=models.ForeignKey(Personnel,on_delete=models.CASCADE,null=True)
    site=models.ForeignKey(Site,on_delete=models.CASCADE,null=True)
    titre_rapport=models.CharField(max_length=150,null=True)
    description = RichTextField(null=True) # Utilisation de CKEDITOR pour le champ de contenu
    date=models.DateField()
    STATUT_CHOICES = [
        ('Brouillon', 'Brouillon'),
        ('En attente', 'En attente de validation'),
        ('Valide', 'Validé'),
        ('Refuse', 'Refusé'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='Brouillon')

    def __str__(self):
        return self.titre_rapport if self.titre_rapport else "Nom non spécifié"
# 6
class Typemateriel(models.Model):
    nom_type_materel=models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.nom_type_materel if self.nom_type_materel else "Nom non spécifié"
# 7
class Materiel(models.Model):
    site=models.ForeignKey(Site,on_delete=models.CASCADE,null=True) 
    nom_materiel=models.CharField(max_length=100,null=True)
    type_materiel=models.ForeignKey(Typemateriel,on_delete=models.CASCADE,null=True) 
    quantite_materiel=models.CharField(max_length=100,null=True)
    qualite=models.CharField(max_length=100,null=True)
    date_d_enregistrement=models.DateField(null=True) 
       
    def __str__(self) :
        return self.nom_materiel if self.nom_materiel else "Nom non spécifié"   



# 8
class Perdieme(models.Model) :
    personne_receveur=models.ForeignKey(Personnel,on_delete=models.CASCADE,null=True)
    site=models.ForeignKey(Site,on_delete=models.CASCADE,null=True)
    description= models.CharField(max_length=100,null=True)
    montant=models.IntegerField()
    date_transaction=models.DateField()
    code_transaction_numero_bordereau=models.CharField(max_length=100,null=True)
 
    def __str__(self):
        return self.description if self.description else "Nom non spécifié"

# 9
class PerdiemeValidation(models.Model):
    perdieme = models.ForeignKey(Perdieme, on_delete=models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    date_validation = models.DateField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.personnel} - {self.perdieme}"
    
    
    
    
    
    

    
    