from .models import Cycle, Evaluation, Matiere, Classe, Eleve, Classe_Matiere, Enseignant, Resultat, Note
from django.db.models import Avg
from orientation.models import Filiere, Filiere_Matiere


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

# def predict_orientation(eleve):
#     """
#     Fonction pour prédire l'orientation d'un élève en fonction de ses notes dans les matières et des critères d'admission des filières.
#     """
#     # Récupération de toutes les filières avec leurs critères d'admission
#     filieres = Filiere.objects.prefetch_related('filiere_matiere_set').all()
#     # filieres = []
#     # Initialisation du dictionnaire pour stocker les moyennes par matière de l'élève
#     moyennes_par_matiere = {}

#     # Calcul des moyennes par matière pour cet élève
#     for classe_matiere in eleve.classe.matiere.all():
#         # Récupération des résultats associés à cette classe_matiere
#         resultats = Resultat.objects.filter(classematiere_id=classe_matiere)

#         # Calcul de la moyenne des notes pour cette classe_matiere et cet élève
#         moyenne = Note.objects.filter(
#             eleve_id=eleve,
#             resultat_id__in=resultats
#         ).aggregate(moyenne=Avg('note'))['moyenne']

#         # Stockage de la moyenne par matière dans le dictionnaire
#         moyennes_par_matiere[classe_matiere.matiere_id] = moyenne

#     # Détermination de la filière prédite pour cet élève
#     filiere_predite = None
#     for filiere in filieres:
#         filiere_acceptee = True
#         for filiere_matiere in filiere.filiere_matiere_set.all():
#             # Vérification si l'élève a les notes requises pour chaque matière de la filière
#             if moyennes_par_matiere.get(filiere_matiere.matiere_id) is None or \
#                     moyennes_par_matiere[filiere_matiere.matiere_id] < filiere_matiere.note:
#                 filiere_acceptee = False
#                 break
#         if filiere_acceptee:
#             filiere_predite = filiere.name
#             break

#     return filiere_predite
