# -*- coding: utf-8 -*-
#  Copyright (c) 2019-2021 Ivan LUCAS.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django.forms import ModelForm
from core.forms.base import FormulaireBase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset
from crispy_forms.bootstrap import Field
from core.models import CommandeModele
from core.utils.utils_commandes import Commandes


class Formulaire(FormulaireBase, ModelForm):

    class Meta:
        model = CommandeModele
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'modeles_commandes_form'
        self.helper.form_method = 'post'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        # Définir comme valeur par défaut
        self.fields["defaut"].label = "Définir comme modèle par défaut"
        if len(CommandeModele.objects.all()) == 0 or self.instance.defaut == True:
            self.fields["defaut"].initial = True
            self.fields["defaut"].disabled = True

        # Affichage
        self.helper.layout = Layout(
            Commandes(annuler_url="{% url 'modeles_commandes_liste' %}"),
            Fieldset("Généralités",
                Field("nom"),
                Field("restaurateur"),
                Field("defaut"),
            ),
            Fieldset("Structure associée",
                Field("structure"),
            ),
        )
