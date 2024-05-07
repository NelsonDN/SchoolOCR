from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Classe_Matiere, Enseignant

class EnseignantCreationForm(UserCreationForm):
    username = forms.CharField(label="Nom de l'enseignant")  
    classe_matiere = forms.ModelMultipleChoiceField(queryset=Classe_Matiere.objects.filter(user__isnull=True),
                                label= "Assigner les matières dans les classes à un enseignant",
                                required=False,)

    class Meta:
        model = Enseignant
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['classe_matiere'].queryset = Classe_Matiere.objects.filter(user__isnull=True)


class EnseignantEditForm(forms.ModelForm):
    classe_matiere = forms.ModelMultipleChoiceField(queryset=None, required=False)

    class Meta:
        model = Enseignant
        fields = ['username', 'email', 'classe_matiere']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Récupérer les matières où user est null ou égal à l'utilisateur en question
        user = kwargs['instance']
        queryset = Classe_Matiere.objects.filter(user__isnull=True) | Classe_Matiere.objects.filter(user=user)
        self.fields['classe_matiere'].queryset = queryset