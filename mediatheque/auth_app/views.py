from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm, CreationLivreForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from auth_app.models import Livre


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
    if request.method =='POST':
        form = CreationLivreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = CreationLivreForm()

    Livres = Livre.objects.all()
    return render(request, 'accueil.html',{'CreationLivre':form, 'Livres': Livres})

def deconnexion(request):
    logout(request)
    return redirect('connexion')

# Modifier un livre
@login_required
def modifier_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if request.method == 'POST':
        form = CreationLivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            return redirect('accueil')  # Redirige vers la liste des livres
    else:
        form = CreationLivreForm(instance=livre)  # Pré-remplit le formulaire avec les données existantes

    return render(request, 'modifier_livre.html', {'form': form, 'livre': livre})

# Supprimer un livre
@login_required
def supprimer_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if request.method == 'POST':  # Confirmation avant suppression
        livre.delete()
        return redirect('accueil')

    return render(request, 'supprimer_livre.html', {'livre': livre})


def liste_livres_publique(request):
    Livres = Livre.objects.all()
    return render(request, 'liste_livres_publique.html',{'Livres':Livres})