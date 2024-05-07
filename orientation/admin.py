from django.contrib import admin
from .models import Filiere, Filiere_Matiere
from schoolmanage.models import Matiere
# admin.site.register(Filiere_Matiere)

# Register your models here.
class MatiereInline(admin.TabularInline):
    model = Filiere.matiere.through
    fields = ('matiere_id','note')

@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    # fields = ['name', 'effectif', 'cycle', 'matiere']
    # fieldsets = [
    #     ('Informatios classe', {'fields': ['name', 'effectif'] }),
    #     ('Informations', {'fields': ['cycle',]})
    # ]
    
    list_display = ('name', 'slug')
    list_per_page = 10
    inlines = [MatiereInline]