# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

import logging
from django.http import Http404
from core.models import Rattachement
logger = logging.getLogger(__name__)
from portail.views.base import CustomView
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from core.models import Structure, PortailMessage
from django.db.models import Q, Count


class View(CustomView, TemplateView):
    menu_code = "portail_contact"
    template_name = "portail/contact.html"
    def get_object(self):
        """Récupérer l'objet famille ou individu selon l'utilisateur"""
        if hasattr(self.request.user, 'famille'):
            return self.request.user.famille
        elif hasattr(self.request.user, 'individu'):
            return self.request.user.individu
        else:
            raise Http404("Utilisateur non reconnu.")

    def get_famille_object(self):
        if hasattr(self.request.user, 'famille'):
            return self.request.user.famille
        elif hasattr(self.request.user, 'individu'):
            rattachement = Rattachement.objects.filter(individu=self.request.user.individu).first()
            if rattachement.famille and rattachement.titulaire == 1:
                return rattachement.famille
        return None

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data(**kwargs)
        context['page_titre'] = _("Contact")
        famille = self.get_famille_object()

        if famille:

            # Importation de toutes les structures
            liste_structures = Structure.objects.filter(messagerie_active=True).order_by("nom")

            # Structures avec messagerie
            context['liste_structures_messagerie'] = [structure for structure in liste_structures if structure.messagerie_active]

            # Structures avec coordonnées
            context['liste_structures_coords'] = [structure for structure in liste_structures if structure.afficher_coords]

            # Importation du nombre de messages non lus (regroupement par structure)
            context['dict_messages_non_lus'] = {valeur["structure"]: valeur["nbre"] for valeur in PortailMessage.objects.values("structure").filter(famille=famille, utilisateur__isnull=False, date_lecture__isnull=True).annotate(nbre=Count('pk'))}

        return context
