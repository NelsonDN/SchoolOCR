from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm


def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username = username, password = password )
        
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin:index')
            else:
                login(request, user)
                return redirect('schoolmanage:enseignants')       
        
        else:
            messages.info(request, "Identifiant ou mot de passe incorrect")
    
    form = AuthenticationForm()
    
    return render(request, "accounts/login.html", {"form": form})
            

def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("schoolmanage:home")
    else:
        form = CreateUserForm()    

    return render(request, "accounts/register.html", {"form": form})
    
def logout_user(request):
    logout(request)
    return redirect('schoolmanage:home')