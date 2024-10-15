from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
# from .forms import ProfileForm,LoginForm,FormTache
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import *

from .forms import *
from django.db.models import Sum
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from datetime import timedelta
from .utils import enregistrer_action


def index(request):
    aujourd_hui = now().date()

    # Utilisateurs connectés aujourd'hui
    utilisateurs_connectes = Personnel.objects.filter(user__last_login__date=aujourd_hui)
    nom_utilisateurs_connectes = [personnel.nom_prenom for personnel in utilisateurs_connectes]  # Liste des noms d'utilisateurs connectés

    # Total des projets terminés
    projets_termines = Projet.objects.filter(status='termine')
    noms_projets_termines = [(projet.nom_projet, projet.finance_par.nom_societe) for projet in projets_termines]  # Liste des projets terminés avec financeurs

    # Projets en cours
    projets_en_cours = Projet.objects.filter(status='en_cours')  # Retourne un QuerySet
    noms_projets_en_cours = [(projet.nom_projet, projet.finance_par.nom_societe) for projet in projets_en_cours]  # Génère une liste de tuples avec deux éléments

    # Actions réalisées au cours des 7 derniers jours
    derniere_semaine = now() - timedelta(days=1)
    actions_recentes = UserActivity.objects.filter(timestamp__gte=derniere_semaine)
    descriptions_actions = [action.action for action in actions_recentes]  # Liste des descriptions d'actions récentes

    context = {
        'utilisateurs_connectes': utilisateurs_connectes.count(),
        'nom_utilisateurs_connectes': nom_utilisateurs_connectes,
        'projets_termines': projets_termines.count(),
        'noms_projets_termines': noms_projets_termines,
        'projets_en_cours': projets_en_cours.count(),
        'noms_projets_en_cours': noms_projets_en_cours,
        'descriptions_actions': descriptions_actions,
    }

    enregistrer_action(request.user, "L'utilisateur a accédé à la page d'action")
    return render(request, 'index.html', context)


def register(request):
    profil_form=ProfileForm(request.POST or None, request.FILES)
    if (request.method=='POST'):
        if (profil_form.is_valid()):
            nom_utilisateur=profil_form.cleaned_data['nom_utilisateur']
            mots_de_pass=profil_form.cleaned_data['mots_de_pass']
            mots_de_pass1=profil_form.cleaned_data['mots_de_pass1']
            nom_prenom=profil_form.cleaned_data['nom_prenom']
            
            date_naissance=profil_form.cleaned_data['date_naissance']
            genre=profil_form.cleaned_data['genre']
            role=profil_form.cleaned_data['role']
            telephone=profil_form.cleaned_data['telephone']
            address=profil_form.cleaned_data['address']
            date_enre=profil_form.cleaned_data['date_enre']
            if (mots_de_pass==mots_de_pass1):
                user=User.objects.create_user(username=nom_utilisateur, password=mots_de_pass)

                user.first_name=nom_prenom
                user.last_name=nom_prenom
                
                user.save()
                group = Group.objects.get_or_create(name= "Technicien")
                user.groups.add(group[0])
                profil=Personnel(
                        user=user,
                        nom_prenom=nom_prenom,
                        
						date_naissance=date_naissance,
						genre=genre,
                        role=role,
						address=address,
						telephone=telephone,
                        date_enre=date_enre).save()
                if user:
                    login(request, user)
                    return redirect(index)
                else:
                    return redirect(login_view)
            else: 
                profil_form=ProfileForm(request.FILES)
                return render(request, 'register.html',locals())
    return render(request, 'register.html',locals())
    

def login_view(request):
    Connexion_form=ConnexionForm(request.POST or None)
    msg=None
    if request.method=='POST':
        if Connexion_form.is_valid():
            nom_utilisateur=Connexion_form.cleaned_data.get('nom_utilisateur')
            mots_de_pass=Connexion_form.cleaned_data.get('mots_de_pass')
            user=authenticate(username=nom_utilisateur,password=mots_de_pass)


            if user:#si l'objet existe 


                login(request, user)
                groups = [group.name for group in user.groups.all()]
                # if user.is_superuser or 'personnel' in groups:
                #      return redirect(index) #on connecte l'utilisateur
                if user.is_superuser or 'Chef' in groups:
                    return redirect(tableau_projets) #on connecte l'utilisateur
                if 'Responsable' in groups:
                    return redirect(tableau_projets) #on connecte l'utilisateur
                if 'Technicien' in groups:
                    return redirect(tableau_projets) #on connecte l'utilisateur
                
            
            else:
                Connexion_form=ConnexionForm()
        else:
            Connexion_form=ConnexionForm()
            return render(request, 'login.html', locals())
    return render(request, 'login.html', locals())
        
def home(request):
    return render(request,'index.html')
def liste_des_personnel(request):
    personnels=Personnel.objects.all()
    return render(request,'liste_personnel.html',{'personnels': personnels})  
def ajouter_personnel(request):
    if request.method=='POST':
        form=Personnel_form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('liste_personnel')    
    else:
        form=Personnel_form()
    return render(request,'personnel_form.html',{'form':form})      
def edit_personnel(request,pk):
    personnels=get_object_or_404(Personnel,pk=pk)
    if request.method=='POST':
        form=Personnel_form(request.POST,instance=personnels)
        if form.is_valid():
            form.save()
            return redirect('liste_personnel')
    else:
        form=Personnel_form(instance=personnels)

    return render(request,'personnel_form.html',{'form':form})

def liste_site(request):
    sites=Site.objects.all()
    # Check if the user is part of 'Chef' or 'Admin' groups or is a superuser
    is_chef = request.user.groups.filter(name='Chef').exists()
    is_admin = request.user.groups.filter(name='Admin').exists() or request.user.is_superuser

    # Pass variables to the context
    context = {
        'sites': sites,
        'is_chef': is_chef,
        'is_admin': is_admin,
    }
    
    return render(request,'site.html',context)
def Ajouter_site(request):

    if request.method=='POST':
        form=Site_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_site')
    else:
        form=Site_form()

    return render(request,'creer_site.html',{'form':form})    

def edit_site(request,pk):
    sites=get_object_or_404(Projet,pk=pk)
    if request.method=='POST':
        form=Site_form(request.POST,instance=sites)
        if form.is_valid():
            form.save()
            return redirect('liste_site')
    else:
        form=Site_form(instance=sites)

    return render(request,'creer_site.html',{'form':form})     

def liste_financement(request):
    societes=Financement.objects.all()
    return render(request,'financement.html',{'societes':societes})
def Ajouter_societe(request):

    if request.method=='POST':
        form=Financement_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_societe')
    else:
        form=Financement_form()

    return render(request,'Ajouter_societe.html',{'form':form})    

def edit_site(request,pk):
    sites=get_object_or_404(Projet,pk=pk)
    if request.method=='POST':
        form=Site_form(request.POST,instance=sites)
        if form.is_valid():
            form.save()
            return redirect('listedesprojet')
    else:
        form=Site_form(instance=sites)

    return render(request,'creer_site.html',{'form':form})     

   

def liste_des_projets(request):
    projets = Projet.objects.all()
   
    # Check if the user is part of 'Chef' or 'Admin' groups or is a superuser
    is_chef = request.user.groups.filter(name='Chef').exists()
    is_admin = request.user.groups.filter(name='Admin').exists() or request.user.is_superuser

    # Pass variables to the context
    context = {
        'projets': projets,
        'is_chef': is_chef,
        'is_admin': is_admin,
    }
    
    return render(request, 'projet.html', context)

def creer_projet(request):
    if request.method=='POST':
        form=Projet_form(request.POST)
        if form.is_valid():
            form.save() 
           
            
        return redirect('listedesprojet')
    else:
        form=Projet_form()

    return render(request,'projet_form.html',{'form':form})    

def edit_projet(request,pk):
    projets=get_object_or_404(Projet,pk=pk)
    if request.method=='POST':
        form=Projet_form(request.POST,instance=projets)
        if form.is_valid():
            form.save()
            return redirect('listedesprojet')
    else:
        form=Projet_form(instance=projets)

    return render(request,'projet_form.html',{'form':form})

def liste_materiel(request):

    materiels = Materiel.objects.all()

    is_chef_or_admin = request.user.groups.filter(name__in=['Chef', 'Admin']).exists() or request.user.is_superuser

    # Passer les informations au template via le contexte
    context = {
        'materiels': materiels,
        'is_chef_or_admin': is_chef_or_admin,
    }

    return render(request, 'materiel.html', context)

def ajouter_materiel(request):
    if request.method=='POST':
        form=Materiel_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_materiel')
    else:
        form=Materiel_form()

    return render(request,'materiel_form.html',{'form':form})    

def editer_materiel(request,pk):
    materiels=get_object_or_404(Materiel,pk=pk)
    if request.method=='POST':
        form=Materiel_form(request.POST,instance=materiels)
        if form.is_valid():
            form.save()
            return redirect('liste_materiel')
    else:
        form=Materiel_form(instance=materiels)

    return render(request,'materiel_form.html',{'form':form})   


def liste_perdieme(request):
    # Récupérer tous les perdiemes
    perdiemes = Perdieme.objects.all()

    # Vérifier si l'utilisateur est dans certains groupes
    is_technicien_or_responsable = request.user.groups.filter(name__in=['Technicien', 'Responsable']).exists()
    is_chef_or_admin = request.user.groups.filter(name__in=['Chef', 'Admin']).exists() or request.user.is_superuser

    # Passer les informations au template via le contexte
    context = {
        'perdiemes': perdiemes,
        'is_technicien_or_responsable': is_technicien_or_responsable,
        'is_chef_or_admin': is_chef_or_admin,
    }

    return render(request, 'perdieme.html', context)

def edit_perdiem(request,pk):
    perdiemes=get_object_or_404(Perdieme,pk=pk)
    if request.method=='POST':
        form=Perdieme_Form(request.POST,instance=perdiemes)
        if form.is_valid():
            form.save()
            return redirect('listeperdieme')
    else:
        form=Perdieme_Form(instance=perdiemes)

    return render(request,'perdieme_form.html',{'form':form})

def ajouter_perdieme(request):
    if request.method=='POST':
        form=Perdieme_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listeperdieme')
    else:
        form=Perdieme_Form()

    return render(request,'perdieme_form.html',{'form':form})        


def tableaubord(request):
    # Vérifier si l'utilisateur est responsable, chef ou admin
    is_technicien=request.user.groups.filter(name='Technicien').exists()
    
    is_responsable = request.user.groups.filter(name='Responsable').exists()
    is_chef_or_admin = request.user.groups.filter(name__in=['Chef', 'Admin']).exists()
    is_chef_or_responsable = request.user.groups.filter(name__in=['Chef', 'Responsable']).exists()

    context = {
        'is_technicien':is_technicien,
 
        'is_responsable': is_responsable,
        'is_chef_or_admin': is_chef_or_admin,
        'is_chef_or_responsable': is_chef_or_responsable,
    }

    return render(request, 'tableaubord.html', context)
 
def responsables(request):
    return render(request,'chef_equipe.html')    



def liste_rapport(request):
    rapports = Rapport.objects.all()

    # Vérifier si l'utilisateur appartient au groupe 'Chef' ou s'il est superutilisateur
    is_chef_or_admin = request.user.groups.filter(name='Chef').exists() or request.user.is_superuser

    return render(request, 'liste_rapport.html', {
        'rapports': rapports,
        'is_chef_or_admin': is_chef_or_admin  # Passer l'information au template
    })    
def est_chef(user):
    return user.personnel.role== 'Responsable'
def est_chef(user):
    return user.personnel.role == 'Chef'
def is_chef_or_admin(user):
    return user.groups.filter(name__in=['Chef', 'Admin']).exists()

def valider_ou_refuser_rapport(request, rapport_id):
    rapport = get_object_or_404(Rapport, id=rapport_id)
    
    if request.method == 'POST':
        statut = request.POST.get('statut')
        if statut in ['Valide', 'Refuse']:
            rapport.statut = statut
            rapport.save()
            messages.success(request, f'Le rapport a été {statut.lower()} avec succès.')
        return redirect('listerapport')  # Redirige après modification du statut

    return render(request, 'valider_ou_refuser.html', {'rapport': rapport})





def edit_rapport(request, pk):
    rapport = get_object_or_404(Rapport, pk=pk)

    # Vérifier que l'utilisateur est le créateur du rapport ou un Chef
    if (rapport.personnel.user != request.user and 
        (not hasattr(request.user, 'personnel') or request.user.personnel.role != 'Chef') and 
        not request.user.is_superuser and 
        rapport.statut in ['Valide', 'Refuse']):
        return redirect('accueil')  # Rediriger si l'utilisateur n'est pas autorisé

    exclude_fields = []
    # Vérifier le rôle de l'utilisateur pour exclure le champ statut si nécessaire
    if (not request.user.is_superuser and 
        (request.user.groups.filter(name='Technicien').exists() or 
         request.user.groups.filter(name='Responsable').exists())):
        exclude_fields.append('statut')

    if request.method == 'POST':
        form = Rapport_Form(request.POST, instance=rapport, exclude_fields=exclude_fields)
        if form.is_valid():
            form.save()
            return redirect('listerapport')  # Rediriger vers la liste des rapports
    else:
        form = Rapport_Form(instance=rapport, exclude_fields=exclude_fields)

    return render(request, 'rapport.html', {'form': form})


def rapport_view(request):
    # Récupérer les groupes de l'utilisateur
    user_groups = request.user.groups.values_list('name', flat=True)

    # Déterminer si l'utilisateur appartient aux groupes 'Responsable' ou 'Technicien'
    is_responsable_or_technicien = 'Responsable' in user_groups or 'Technicien' in user_groups

    if request.method == 'POST':
        # Exclure le champ 'statut' si l'utilisateur est dans un des groupes spécifiques
        if is_responsable_or_technicien:
            form = Rapport_Form(request.POST, exclude_fields=['statut'])
        else:
            form = Rapport_Form(request.POST)
        
        if form.is_valid():
            rapport = form.save(commit=False)
            try:
                # Récupérer l'instance de Personnel liée à l'utilisateur connecté
                personnel = Personnel.objects.get(user=request.user)
                rapport.personnel = personnel
                rapport.save()
                return redirect('listerapport')  # Rediriger vers la liste des rapports
            except Personnel.DoesNotExist:
                # Gérer le cas où l'utilisateur n'est pas associé à un Personnel
                form.add_error(None, "Votre compte n'est pas associé à un personnel.")
    else:
        # Pour un GET, on affiche le formulaire avec ou sans le champ 'statut'
        if is_responsable_or_technicien:
            form = Rapport_Form(exclude_fields=['statut'])
        else:
            form = Rapport_Form()

    return render(request, 'rapport.html', {'form': form})

def rapport(request):
    return render(request,'rapport.html') 

def valider_rapport(request, id):
    rapport = get_object_or_404(Rapport, id=id)

    # Vérifier que l'utilisateur est un Chef
    if not hasattr(request.user, 'personnel') or request.user.personnel.role != 'Chef':
        messages.error(request, "Vous n'avez pas l'autorisation de valider ce rapport.")
        return redirect('home')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'valider':
            rapport.statut = 'Valide'
            messages.success(request, "Le rapport a été validé.")
        elif action == 'refuser':
            rapport.statut = 'Refuse'
            messages.success(request, "Le rapport a été refusé.")
        rapport.save()

    return redirect('listerapport')


def print_materiel(request):
    materiels = Materiel.objects.all()
    return render(request, 'print.html', {'materiels': materiels})


def listeprojet(request):
    projets = Projet.objects.all()
    
    is_chef_or_admin = request.user.groups.filter(name__in=['Chef', 'Admin']).exists() or request.user.is_superuser

    # Passer les informations au template via le contexte
    context = {
        'projets': projets,
        'is_chef_or_admin': is_chef_or_admin,
    }

    return render(request, 'touslesprojet.html', {'projets': projets})
def projet_detail(request, id):
    projet = get_object_or_404(Projet, id=id)
    personnels = Personnel.objects.filter(projet=projet)
    rapports = Rapport.objects.filter(projet=projet)
    materiels = Materiel.objects.filter(projet=projet)
    perdiems = Perdieme.objects.filter(projet=projet)

    context = {
        'projet': projet,
        'personnels': personnels,
        'rapports': rapports,
        'materiels': materiels,
        'perdiems': perdiems,
    }
    return render(request, 'projet_detail.html', context)


def validate_perdieme(request, id):
    perdieme = get_object_or_404(Perdieme, id=id)
    
    # Utiliser le related_name défini dans le modèle Personnel
    personnel = request.user.personnel_user  # Accéder à l'objet Personnel lié

    # Vérifiez si le personnel de la requête correspond au personnel du per diem
    if perdieme.personnel != personnel:
        # Redirigez vers une page d'erreur ou affichez un message d'erreur
        return redirect('error_page')  # Changez ceci en l'URL de votre choix

    validation, created = PerdiemeValidation.objects.get_or_create(perdieme=perdieme, personnel=personnel)

    if request.method == 'POST':
        form = PerdiemeValidationForm(request.POST, instance=validation)
        if form.is_valid():
            form.save()
            return redirect('listeperdi')  # Changez ceci en l'URL de votre choix
    else:
        form = PerdiemeValidationForm(instance=validation)

    return render(request, 'validate_perdieme.html', {'form': form, 'perdieme': perdieme})

    class Meta:
        model = PerdiemeValidation
        fields = ['is_validated']
        labels = {
            'is_validated': 'Validation',
        }
        widgets = {
            'is_validated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        
        
def perdieme_list(request):
    # Récupérer tous les objets Perdieme
    perdiemes = Perdieme.objects.all()
    
    # Préparer les données pour le template
    perdieme_data = []
    for perdieme in perdiemes:
        validations = PerdiemeValidation.objects.filter(perdieme=perdieme)
        is_validated = any(validation.is_validated for validation in validations)
        perdieme_data.append({
            'perdieme': perdieme,
            'is_validated': is_validated,
        })
    
    context = {
        'perdieme_data': perdieme_data,
    }
    
    return render(request, 'perdieme_list.html', context)


def Actualites(request):
    
    render(request, 'actualite.html')
    
def tableaubordchef(request):
    return render(request, 'tableaubordchef.html') 
    
    
def tableaubordtech(request):
    return render(request, 'tableaubordtech.html')
def projetdetail(request):
    return render(request, 'touslesprojet.html')


def perdiems_totals_view(request):
    # Total des perdiems par personne
    perdiems_par_personne = Perdieme.objects.values('personne_receveur').annotate(total_perdiem=Sum('montant'))

    # Total des perdiems par site
    perdiems_par_site = Perdieme.objects.values('site').annotate(total_perdiem=Sum('montant'))

    # Calcul du total des perdiems pour toutes les personnes et tous les sites
    total_perdiems_personnes = Perdieme.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    total_perdiems_sites = total_perdiems_personnes  # Identique, car il s'agit du même montant total

    context = {
        'perdiems_par_personne': perdiems_par_personne,
        'perdiems_par_site': perdiems_par_site,
        'total_perdiems_personnes': total_perdiems_personnes,
        'total_perdiems_sites': total_perdiems_sites,
    }

    return render(request, 'perdiems_totals.html', context)




def tableau_projets(request):
    aujourd_hui = timezone.now().date()

    # Récupérer tous les projets en cours
    projets_en_cours = Projet.objects.filter(date_debut__lte=aujourd_hui, date_fin__gte=aujourd_hui)

    # Récupérer tous les projets terminés
    projets_termines = Projet.objects.filter(date_fin__lt=aujourd_hui)

    # Vérifier si l'utilisateur est dans certains groupes
    is_responsable = request.user.groups.filter(name='Responsable').exists()
    is_chef = request.user.groups.filter(name='Chef').exists()
    is_admin = request.user.is_superuser  # Vérifie si l'utilisateur est admin

    projets_details_en_cours = []
    for projet in projets_en_cours:
        # Récupérer les sites d'implémentation pour ce projet
        sites = Site.objects.filter(finance_par=projet.finance_par)
        total_personnels = Personnel.objects.filter(site__in=sites).count()

        # Calculer le total des perdiems pour les sites de ce projet
        total_perdiems = Perdieme.objects.filter(site__in=sites).aggregate(Sum('montant'))['montant__sum'] or 0

        projets_details_en_cours.append({
            'projet': projet,
            'sites': sites,
            'total_personnels': total_personnels,
            'total_perdiems': total_perdiems,  # Ajout du total des perdiems pour le projet
        })

    projets_details_termines = []
    for projet in projets_termines:
        # Récupérer les sites d'implémentation pour ce projet
        sites = Site.objects.filter(finance_par=projet.finance_par)

        # Calculer le total des perdiems pour les sites de ce projet
        total_perdiems = Perdieme.objects.filter(site__in=sites).aggregate(Sum('montant'))['montant__sum'] or 0

        projets_details_termines.append({
            'projet': projet,
            'sites': sites,
            'total_perdiems': total_perdiems,  # Ajout du total des perdiems pour le projet terminé
        })

    # Passer les informations au template via le contexte
    context = {
        'projets_details_en_cours': projets_details_en_cours,
        'projets_details_termines': projets_details_termines,
        'is_responsable': is_responsable,
        'is_chef': is_chef,
        'is_admin': is_admin,
    }

    return render(request, 'tableaubord.html', context)

def est_responsable(user):
    return user.groups.filter(name='Responsable').exists()

def est_chef(user):
    return user.groups.filter(name='Chef').exists()
