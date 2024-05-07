from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# from django.apps import apps 
# model = apps.get_model("orientation", "Filiere")

class Cycle(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Cycle"
        verbose_name_plural = "Cycles"

class Evaluation(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Evaluation"
        verbose_name_plural = "Evaluations"

class Matiere(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"

class Classe(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")
    effectif = models.IntegerField(verbose_name= "Effectif")
    cycle = models.ForeignKey(Cycle, on_delete=models.DO_NOTHING, verbose_name= "Cycle")
    matiere = models.ManyToManyField(Matiere, through='Classe_Matiere')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

class Classe_Matiere(models.Model):
    classe_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    matiere_id = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    coefficient = models.IntegerField(default=1, verbose_name= "Coefficient")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Enseignant")

    def __str__(self):
        return f"{self.matiere_id.name} - {self.classe_id.name}"


class Eleve(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")
    classe = models.ForeignKey(Classe, on_delete=models.DO_NOTHING, verbose_name= "Classe")
    matricule = models.CharField(max_length=64, unique=True, verbose_name= "Matricule")
    filiere = models.CharField(max_length=200, null=True, blank=True, verbose_name="Résultat prédiction")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Eleve"
        verbose_name_plural = "Eleves"  

class Enseignant(User):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username  
    
class Resultat(models.Model):
    classematiere_id = models.ForeignKey(Classe_Matiere, on_delete=models.CASCADE)
    evaluation_id = models.ForeignKey(Evaluation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.classematiere_id} - {self.evaluation_id.name}"
    class Meta:
        verbose_name = "Resultat"
        verbose_name_plural = "Resultats"  
    
class Note(models.Model):
    eleve_id = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    note = models.TextField(null=True, verbose_name= "Note")
    resultat_id = models.ForeignKey(Resultat, on_delete=models.CASCADE)

    def __str__(self):
        return self.eleve_id.name
    
    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Note"  