from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from schoolmanage.models import Matiere

class Filiere(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")
    slug = models.CharField(max_length=64, unique=True, verbose_name= "Slug")
    matiere = models.ManyToManyField(Matiere, through='Filiere_Matiere')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"

class Filiere_Matiere(models.Model):
    filiere_id = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    matiere_id = models.ForeignKey(Matiere, on_delete=models.CASCADE, verbose_name= "Matiere")
    note = models.DecimalField(max_digits=5, decimal_places=2, verbose_name= "Note minimal")


    def __str__(self):
        return f"{self.filiere_id.slug}"