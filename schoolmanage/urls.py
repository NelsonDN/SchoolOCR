from django.urls import path
from . import views

app_name = "schoolmanage"

urlpatterns = [
    path('', views.home, name = 'home'),
    path('direction/', views.direction, name = 'direction'),
    path('parents/', views.parents, name = 'parents'),
    path('enseignants/', views.enseignants, name = 'enseignants'),
    path('classe/matieres/<int:classe_id>/', views.show_matiere, name = 'show_matiere'),
    path('matiere/evaluation/<int:matiere_id>/', views.show_evaluation, name = 'show_evaluation'),
    path('evaluation/note/index/<int:evaluation_id>/', views.index_note, name = 'index_note'),
    path('evaluation/note/edit/<int:eleve_note_id>/', views.edit_note, name = 'edit_note'),
    path('evaluation/note/form/<int:evaluation_id>/', views.add_note, name = 'add_note')

]

