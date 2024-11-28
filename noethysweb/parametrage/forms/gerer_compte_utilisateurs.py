#  Copyright (c) 2024 GIP RECIA.
#  Noethysweb, application de gestion multi-activités.
#  Distribué sous licence GNU GPL.

from django import forms
from core.forms.base import FormulaireBase
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Hidden, Submit, HTML, Fieldset, Div, ButtonHolder
from crispy_forms.bootstrap import Field, InlineRadios
from core.utils.utils_commandes import Commandes

LISTE_RUBRIQUES = [
    ("Compte Utilisateurs", ["compte_famille", "compte_individu"]), ]


class Formulaire(FormulaireBase, forms.Form):
    def __init__(self, *args, **kwargs):
        super(Formulaire, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'compte_parametres_form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'

        # Initialisation du layout
        self.helper.layout = Layout()
        self.helper.layout.append(Commandes(annuler_url="{% url 'gerer_compte_utilisateurs' %}", ajouter=False))

        # Création des fields avec valeurs initiales basées sur les sessions
        compte_famille_active = kwargs.get('compte_famille_active', False)
        compte_individu_active = kwargs.get('compte_individu_active', False)

        # Initialize fields with default or session-based initial values
        for titre_rubrique, liste_parametres in LISTE_RUBRIQUES:
            liste_fields = []
            for code_parametre in liste_parametres:
                self.fields[code_parametre] = forms.BooleanField(required=False,
                                                                 initial=kwargs.get(code_parametre, False))
                liste_fields.append(Field(code_parametre))
            self.helper.layout.append(Fieldset(titre_rubrique, *liste_fields))
        self.helper.layout.append(HTML(EXTRA_SCRIPT))

    def clean(self):
        cleaned_data = super().clean()
        compte_individu = cleaned_data.get("compte_individu")
        compte_famille = cleaned_data.get("compte_famille")
        # Validation pour s'assurer qu'un seul champ est sélectionné
        if compte_individu and compte_famille:
            raise forms.ValidationError("Vous ne pouvez sélectionner qu'un seul compte à la fois.")
        return cleaned_data


EXTRA_SCRIPT = """
<script>
window.onload = function() {
    const checkboxIndividu = document.getElementById("id_compte_individu"); 
    const checkboxFamille = document.getElementById("id_compte_famille");  

    console.log("Checkboxes trouvées avec succès"); // Vérifie si les cases à cocher sont trouvées

    checkboxIndividu.addEventListener('change', function() {
            if (this.checked) {
                checkboxFamille.checked = false;
                checkboxFamille.disabled = true;
            } else {
                checkboxFamille.disabled = false;
            }
        });

    checkboxFamille.addEventListener('change', function() {
            if (this.checked) {
                checkboxIndividu.checked = false;
                checkboxIndividu.disabled = true;
            } else {
                checkboxIndividu.disabled = false;
            }
        });
};
</script>
<br>
"""