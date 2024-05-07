from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cycle, Evaluation, Matiere, Classe, Eleve, Classe_Matiere, Enseignant, Resultat, Note
from .forms import EnseignantCreationForm, EnseignantEditForm
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg
from orientation.models import Filiere, Filiere_Matiere
# admin.site.register(Classe_Matiere)

class MatiereInline(admin.TabularInline):
    model = Classe.matiere.through
    fields = ('matiere_id','coefficient')

@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10
    

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    def voir_eleves(self, obj):
        return format_html('<a href="/admin/schoolmanage/eleve/?classe__id__exact={}">Voir élèves</a>'.format(obj.id))
    voir_eleves.allow_tags = True
    voir_eleves.short_description = "Voir élèves"
    
    # fields = ['name', 'effectif', 'cycle', 'matiere']
    fieldsets = [
        ('Informatios classe', {'fields': ['name', 'effectif'] }),
        ('Informations', {'fields': ['cycle',]})
    ]
    
    list_display = ('name', 'effectif', 'cycle', 'voir_eleves')
    list_filter = ['cycle', 'matiere']
    search_fields = ['cycle__name', 'name']
    list_per_page = 10
    inlines = [MatiereInline]


def predict_orientation(eleve):
    """
    Fonction pour prédire l'orientation d'un élève en fonction de ses notes dans les matières et des critères d'admission des filières.
    """
    # Récupérer les critères d'admission pour chaque filière
    filieres = Filiere.objects.prefetch_related('filiere_matiere_set').all()

    # Initialiser un dictionnaire pour stocker les notes moyennes de l'élève dans chaque matière
    moyennes_par_matiere = {}

    # Calculer les moyennes des notes de l'élève dans chaque matière
    for classe_matiere in eleve.classe.classe_matiere_set.all():
        #Récupération des résultats associés à cette classe_matiere
        resultats = Resultat.objects.filter(classematiere_id=classe_matiere)
        notes = Note.objects.filter(eleve_id=eleve, resultat_id__in=resultats)
        # notes = Note.objects.filter(eleve_id=eleve, resultat_id__classematiere=classe_matiere)
        if notes.exists():
            moyenne = sum(float(note.note) for note in notes) / len(notes)
            moyennes_par_matiere[classe_matiere.matiere_id] = moyenne

    # Prédire l'orientation de l'élève en fonction des critères d'admission pour chaque filière
    filiere_predite = None
    meilleur_score = 0
    for filiere in filieres:
        score_filiere = 0
        for filiere_matiere in filiere.filiere_matiere_set.all():
            if filiere_matiere.matiere_id in moyennes_par_matiere:
                if moyennes_par_matiere[filiere_matiere.matiere_id] >= filiere_matiere.note:
                    score_filiere += 1
        if score_filiere > meilleur_score:
            filiere_predite = filiere
            meilleur_score = score_filiere

    return filiere_predite

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    fields = ['name', 'matricule', 'classe']
    
    list_display = ('name', 'classe', 'matricule', 'predict_orientation_link', 'filiere')
    list_filter = ['matricule', 'classe']
    search_fields = ['matricule', 'classe__name']
    list_per_page = 10
    actions = ['predict_orientation_for_selected_students']

    def predict_orientation_link(self, obj):
        return format_html('<a href="{}">Prédire</a>'.format(
            reverse('schoolmanage:predict_orientation', args=[obj.pk])
        ))
    predict_orientation_link.short_description = "Prédiction d'orientation"

    def predict_orientation_for_selected_students(self, request, queryset):
        for eleve in queryset:
            # Code pour la prédiction de l'orientation de chaque élève
            filiere_predite = predict_orientation(eleve)
            # Mettre à jour la filière prédite pour cet élève
            eleve.filiere = filiere_predite
            eleve.save()

    predict_orientation_for_selected_students.short_description = "Prédire l'orientation des élèves sélectionnés"

    def get_actions(self, request):
        # Supprimer toutes les actions par défaut
        actions = super().get_actions(request)
        actions.clear()
        return actions

    def voir_eleves(self, request, queryset):
        # Rediriger vers la vue de liste des élèves
        return HttpResponseRedirect(reverse('admin:schoolmanage_eleve_changelist'))

    voir_eleves.short_description = "Voir élèves"
    
class EnseignantAdmin(admin.ModelAdmin):
    form = EnseignantCreationForm

    list_display = ('nom_enseignant', 'email', 'matiere_enseigne', 'classe')

    def nom_enseignant(self, obj):
        return obj.username
    
    def matiere_enseigne(self, obj):
        classe_matieres = Classe_Matiere.objects.filter(user=obj)
        return ", ".join([f"{classe_matiere.matiere_id.name}" for classe_matiere in classe_matieres])

    def classe(self, obj):
        classe_matieres = Classe_Matiere.objects.filter(user=obj)
        return ", ".join([f"{classe_matiere.classe_id.name}" for classe_matiere in classe_matieres])

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)
    
    def get_form(self, request, obj=None, **kwargs):
        if obj:  # Vérifie si un objet est en cours d'édition
            return EnseignantEditForm
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        classe_matiere_ids = request.POST.getlist('classe_matiere')
        if classe_matiere_ids:
            Classe_Matiere.objects.filter(pk__in=classe_matiere_ids).update(user=obj)
            
admin.site.register(Enseignant, EnseignantAdmin)

@admin.register(Resultat)
class ResultatAdmin(admin.ModelAdmin):
    def voir_eleves_notes(self, obj):
        return format_html('<a href="/admin/schoolmanage/note/?resultat__id__exact={}">Voir les notes des élèves</a>'.format(obj.id))
    voir_eleves_notes.allow_tags = True
    voir_eleves_notes.short_description = "Voir les notes des élèves"

    fields = ['classematiere_id', 'evaluation_id']
    
    list_display = ('classematiere_id', 'evaluation_id', 'voir_eleves_notes')
    search_fields = ['classematiere_id__name', 'evaluation_id__name']
    list_per_page = 10

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    fields = ['eleve_id', 'note']
    
    list_display = ('eleve_id', 'note')
    list_filter = ['note']
    search_fields = ['eleve_id__name']
    list_per_page = 10