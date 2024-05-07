from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cycle, Evaluation, Matiere, Classe, Eleve, Classe_Matiere, Enseignant, Resultat, Note
from .forms import EnseignantCreationForm, EnseignantEditForm
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
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
    

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    fields = ['name', 'matricule', 'classe']
    
    list_display = ('name', 'classe', 'matricule')
    list_filter = ['matricule', 'classe']
    search_fields = ['matricule', 'classe__name']
    list_per_page = 10
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