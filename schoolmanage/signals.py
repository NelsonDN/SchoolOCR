# Dans un fichier signals.py dans votre application
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enseignant, Classe_Matiere

# def update_classe_matiere(sender, instance, created, **kwargs):
#     if created:
#         classe_matiere_ids = instance.classe_matiere.values_list('id', flat=True)
#         Classe_Matiere.objects.filter(pk__in=classe_matiere_ids).update(user=instance)@receiver(post_save, sender=Enseignant)
# @receiver(post_save, sender=Enseignant)
# def update_classe_matiere(sender, instance, created, **kwargs):
#     if created:
#         classe_matiere_ids = instance.cleaned_data.get('classe_matiere')  # Récupère les IDs des matières sélectionnées
#         if classe_matiere_ids:
#             Classe_Matiere.objects.filter(pk__in=classe_matiere_ids).update(user=instance)
#@receiver(post_save, sender=Enseignant)
# def update_classe_matiere(sender, instance, created, **kwargs):
#     if created:
#         request = kwargs['request']
#         data = request.POST  # Obtenir les données de la requête POST
#         print("data")
#         print(data)
#         classe_matiere_ids = data.getlist('classe_matiere')  # Récupérer les IDs des matières sélectionnées
#         print("classeeeeeeeeeeeeeeeeeee")
#         print(classe_matiere_ids)
#         if classe_matiere_ids:
#             Classe_Matiere.objects.filter(pk__in=classe_matiere_ids).update(user=instance)