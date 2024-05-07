from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

# class BookForm(forms.ModelForm):
#     author = forms.ModelChoiceField(queryset= Author.objects.all(), label="Auteur")
    
#     class Meta:
#         model = Book
#         fields = ['title', 'author', 'quantity']
#         labels = {'title': 'Titre', 'quantity': 'Quantité'}

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']