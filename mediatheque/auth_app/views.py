from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from medias.models import Livre, Dvd, Cd
from medias.forms import CreationLivreForm, CreationDvdForm, CreationCdForm
from .forms import CustomUserCreationForm


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
        livre_form = CreationLivreForm(request.POST)
        dvd_form = CreationDvdForm(request.POST)
        cd_form = CreationCdForm(request.POST)

        if livre_form.is_valid():
            form.save()
            return redirect('accueil')
        
        if dvd_form.is_valid():
            dvd_form.save()
            return redirect('accueil')

        if cd_form.is_valid():
            cd_form.save()
            return redirect('accueil')
    else:
        livre_form = CreationLivreForm()
        dvd_form = CreationDvdForm()
        cd_form = CreationCdForm()

    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()

    return render(request, 'accueil.html',{
        'CreationLivre': livre_form,
        'CreationDvd': dvd_form,
        'CreationCd': cd_form,
        'Livres': livres,
        'Dvds': dvds,
        'Cds': cds
        })

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

# Modifier un DVD
@login_required
def modifier_dvd(request, dvd_id):
    dvd = get_object_or_404(Dvd, id=dvd_id)
    if request.method == 'POST':
        form = CreationDvdForm(request.POST, instance=dvd)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = CreationDvdForm(instance=dvd)

    return render(request, 'modifier_dvd.html', {'form': form, 'livre': dvd})

# Supprimer un DVD
@login_required
def supprimer_dvd(request, dvd_id):
    dvd = get_object_or_404(Dvd, id=dvd_id)
    if request.method == 'POST':
        dvd.delete()
        return redirect('accueil')

    return render(request, 'supprimer_dvd.html', {'dvd': dvd})

# Modifier un CD
@login_required
def modifier_cd(request, cd_id):
    cd = get_object_or_404(Cd, id=cd_id)
    if request.method == 'POST':
        form = CreationCdForm(request.POST, instance=cd)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = CreationCdForm(instance=cd)

    return render(request, 'modifier_cd.html', {'form': form, 'livre': cd})

# Supprimer un CD
@login_required
def supprimer_cd(request, cd_id):
    cd = get_object_or_404(Cd, id=cd_id)
    if request.method == 'POST':  # Confirmation avant suppression
        cd.delete()
        return redirect('accueil')

    return render(request, 'supprimer_dvd.html', {'dvd': cd})


def liste_livres_publique(request):
    Livres = Livre.objects.all()
    return render(request, 'liste_livres_publique.html',{'Livres':Livres})

def liste_cds_publique(request):
    Cds = Cd.objects.all()
    return render(request,'liste_cds_publique.html',{'Cds':Cds})

def liste_dvds_publique(request):
    Dvds = Dvd.objects.all()
    return render(request,'liste_dvds_publique.html',{'Dvds':Dvds})
