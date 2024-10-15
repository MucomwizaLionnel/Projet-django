from .utils import enregistrer_action

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Enregistrer l'activité de l'utilisateur pour les requêtes POST
        if request.method == 'POST' and request.user.is_authenticated:
            nom_utilisateur = request.user.username  # ou `request.user.first_name` selon votre modèle
            enregistrer_action(request.user, f"Action POST sur {request.path} par {nom_utilisateur}")

        return response
