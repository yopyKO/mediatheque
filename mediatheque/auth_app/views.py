from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from medias.models import Livre

# Create your views here
def inscription(request):
    if request.method=='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form':form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request,'Nom d\'utilisateur ou mot de passe incorrect')
    return render(request,'connexion.html')

@login_required
def accueil(request):
    return render(request, 'accueil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def ListeLivres(request):
    Livres = Livre.objects.all()
    return render(request, 'connexion.html',{'Livres':Livres})

def ajoutLivre(request):
    if request.method =='POST':
        CreationLivre = CreationLivre(request.POST)
        if CreationLivre.is_valid():
            Livre = Livre()
            Livre.name = CreationLivre.cleaned_data['nom']
            Livre.auteur = CreationLivre.cleaned_data['auteur']
            Livre.save()
            Livres = Livre.objects.all()
            return render(request, 'connexion.html', {'Livres': Livres})
        else:
            CreationLivre = CreationLivre()
            return render(request, 'accueil.html',{'CreationLivre':CreationLivre})