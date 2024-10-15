
from django.urls import path
from .import views 



urlpatterns = [

    path('',views.login_view ,name="login_view" ),
    path('index',views.index ,name='index' ),
    path('register/',views.register ,name='register' ),
    path('home/',views.home,name='home' ),
   
    path('tableau/',views.tableau_projets,name='tableaubord' ),
    # path('chef_equipe/',views.responsables,name='responsables' ),
  
    path('projet/',views.liste_des_projets,name='listedesprojet'),
    path('personnel/',views.liste_des_personnel,name='liste_personnel' ),
    path('Ajouter_personnel/',views.ajouter_personnel,name='AjouterPersonnel' ),
    path('editer_personnel<int:pk>/',views.edit_personnel,name='editerpersonnel'),
    
    path('creer_projet',views.creer_projet,name='creer' ),
    path('editer_projet<int:pk>/',views.edit_projet,name='editprojet'),
    path('editperdiem<int:pk>/',views.edit_perdiem,name='editer'),
   
    path('materiel',views.liste_materiel,name='liste_materiel' ),
    path('Ajouter_un_materiel',views.ajouter_materiel,name='ajoutmateriel' ),
    path('editermat<int:pk>/',views.editer_materiel, name='editerMateriel'),
    path('editerrapport<int:pk>/',views.edit_rapport, name='editerRapport'),
    

    path('print/', views.print_materiel, name='print_materiel'),
    path('perdieme/', views.liste_perdieme, name='listeperdieme'),
    path('Ajoutperdieme/', views.ajouter_perdieme, name='ajouterperdieme'),
    
    path('projet/<int:id>/', views.projet_detail, name='projet_detail'),#le lien qui permer de clique sur les detaill des projet
    path('Validation/<int:id>/', views.validate_perdieme, name='valide'),#le lien de validation de perdieme
    
    path('rapport/<int:rapport_id>/changer-statut/<str:statut>/', views.valider_rapport, name='valide_refuse'),
    path('listeperdi/', views.perdieme_list, name='listeperdi'), #verification des perdieme valider ou non valider
    # path('actualite/', views.Actualites, name='actualites'),
  


    path('rapport',views.rapport_view,name='rapport' ),
    path('listerapport',views.liste_rapport,name='listerapport'),
   
    path('liste_des_site',views.liste_site,name='liste_site'),
    path('Ajouter_site',views.Ajouter_site,name='Ajouter_un_site'),
    path('editer_un_site<int:pk>/',views.edit_site, name='editersite'),

    path('tableaubordchefs/',views.tableaubordchef,name='tableauborddeschef'),
    path('liste_financement',views.liste_financement,name='list_societe'),
    path('Ajouter_societe',views.Ajouter_societe,name='ajout_societe'),
    path('touslesprojet/',views.listeprojet,name='touslesprojet'),
    path('perdiems-totals/', views.perdiems_totals_view, name='perdiems_totals'),

    path('rapport/<int:rapport_id>/valider_ou_refuser/', views.valider_ou_refuser_rapport, name='valider_ou_refuser_rapport'),

    
    

    
   
]