from .models import UserActivity

def enregistrer_action(user, description_action):
    """
    Enregistre une action spécifique effectuée par un utilisateur.
    
    :param user: L'utilisateur qui a effectué l'action.
    :param description_action: Une description de l'action à enregistrer.
    """
    if user.is_authenticated:
        UserActivity.objects.create(
            user=user,
            action=description_action
        )
