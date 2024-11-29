# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.http import HttpResponseRedirect
from django.urls import reverse
from portail.utils import utils_secquest
from core.models import Famille


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # URL pour changer le mot de passe
        url_change_password = reverse("password_change")

        # Oblige la famille ou l'individu à changer son mot de passe
        if request.user.is_authenticated:
            # Vérification pour les utilisateurs de type famille
            if request.user.categorie == "famille" and request.user.force_reset_password and request.path != url_change_password:
                utils_secquest.Generation_secquest(famille=request.user.famille)
                return HttpResponseRedirect(url_change_password)

            # Vérification pour les utilisateurs de type individu
            elif request.user.categorie == "individu" and request.user.force_reset_password and request.path != url_change_password:
                # Ici, assurez-vous de bien gérer la génération de la question de sécurité pour l'individu
                famille = Famille.objects.filter(titulaire_helios_id=request.user.individu).first()
                if famille:
                    utils_secquest.Generation_secquest(famille=famille)  # Génération de la question de sécurité pour la famille associée
                return HttpResponseRedirect(url_change_password)

        return response