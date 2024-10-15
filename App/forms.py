from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.core.exceptions import ValidationError
import datetime

from ckeditor.fields import RichTextField




class ProfileForm(forms.Form):
	#____________pour user___________________#
		nom_utilisateur=forms.CharField(max_length=7)
		mots_de_pass=forms.CharField(max_length=20, widget=forms.PasswordInput)
		mots_de_pass1=forms.CharField(max_length=20, widget=forms.PasswordInput)
		nom_prenom=forms.CharField(max_length=50)
		
	#______________champ pou profil___________#
		date_naissance = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
		genre = forms.CharField(max_length=20)
		role = forms.ChoiceField(choices=[('Choisisez','Choisisez'),('Chef', 'Chef'), ('Responsable', 'Responsable'), ('Technicien', 'Technicien')])
   
		telephone = forms.CharField(max_length=20)
		address = forms.CharField(max_length=20)
		date_enre=forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
class ConnexionForm(forms.Form):
	nom_utilisateur= forms.CharField(widget= forms.TextInput(attrs={
    		'placeholder':'nom utilisateur ',
    		}),label="nom utilisateur :")
	mots_de_pass = forms.CharField(widget= forms.PasswordInput(attrs={
    		'placeholder':'.........',
    		}),label="mots de pass :")
    

class Personnel_form(forms.ModelForm):

    class Meta:
        model=Personnel
        fields='__all__'

class Financement_form(forms.ModelForm):

    class Meta:
        model=Financement
        # fields = ['personnel', 'projet', 'titre_rapport', 'description', 'date']
        fields = '__all__'
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_field(self):
        date = self.cleaned_data['date_field']
        if date:
            try:
                datetime.datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                raise ValidationError('La date doit être au format AAAA-MM-JJ.')
        return date




class Projet_form(forms.ModelForm):
    class Meta:
        model=Projet

        fields = '__all__'

        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_field(self):
        date = self.cleaned_data['date_field']
        if date:
            try:
                datetime.datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                raise ValidationError('La date doit être au format AAAA-MM-JJ.')
        return date



class Site_form(forms.ModelForm):

    class Meta:
        model = Site
        fields = '__all__'
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_date_field(self):
        date = self.cleaned_data['date_field']
        if date:
            try:
                datetime.datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                raise ValidationError('La date doit être au format AAAA-MM-JJ.')
        return date
    

class Materiel_form(forms.ModelForm):

    class Meta:
        model = Materiel
        fields = '__all__'
        widgets = {
            'date_d_enregistrement': forms.DateInput(attrs={'type': 'date'}),
            
        }

    def clean_date_field(self):
        date = self.cleaned_data['date_field']
        if date:
            try:
                datetime.datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                raise ValidationError('La date doit être au format AAAA-MM-JJ.')
        return date
# class Model:
#     def delete(self):
#         print("Instance deleted")

# # Créez une instance de la classe Model
# model_instance = Model()

# # Appelez la méthode delete sur l'instance
# model_instance.delete()

class Perdieme_Form(forms.ModelForm):

    class Meta:
        model = Perdieme
        fields = '__all__'
        widgets = {
            'date_transaction': forms.DateInput(attrs={'type': 'date'}),
            
        }

    def clean_date_field(self):
        date = self.cleaned_data['date_field']
        if date:
            try:
                datetime.datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                raise ValidationError('La date doit être au format AAAA-MM-JJ.')
        return date


class Rapport_Form(forms.ModelForm):

   
    class Meta:
        model = Rapport
        description = RichTextField()
        fields = ['site', 'titre_rapport', 'description', 'date', 'statut']  # Include all fields
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            
        }

    def clean_date_field(self):
        date = self.cleaned_data['date_field']
        if date:
            try:
                datetime.datetime.strptime(str(date), '%Y-%m-%d')
            except ValueError:
                raise ValidationError('La date doit être au format AAAA-MM-JJ.')
        return date
    
     

    def __init__(self, *args, **kwargs):
        # Extraire l'argument exclude_fields s'il est passé
        exclude_fields = kwargs.pop('exclude_fields', None)
        # Appeler le constructeur parent sans l'argument exclude_fields
        super(Rapport_Form, self).__init__(*args, **kwargs)

        # Supprimer les champs spécifiés dans exclude_fields du formulaire
        if exclude_fields:
            for field in exclude_fields:
                if field in self.fields:
                    del self.fields[field]
    
    
class PerdiemeValidationForm(forms.ModelForm):
    class Meta:
        model = PerdiemeValidation
        fields = ['is_validated']
        widgets = {
            'is_validated': forms.CheckboxInput(),
        }
        labels = {
            'is_validated': 'J\'ai reçu le per diem',
        }