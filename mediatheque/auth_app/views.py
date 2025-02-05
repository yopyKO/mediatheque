from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from medias.models import Livre, Dvd, Cd, Media, Emprunt
from medias.forms import CreationLivreForm, CreationDvdForm, CreationCdForm
from mediatheque.models import Membre
from mediatheque.forms import CreationMembreForm
from .forms import CustomUserCreationForm
from django.utils import timezone


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
        membre_form = CreationMembreForm(request.POST)

        if livre_form.is_valid():
            livre_form.save()
            return redirect('accueil')
        
        if dvd_form.is_valid():
            dvd_form.save()
            return redirect('accueil')

        if cd_form.is_valid():
            cd_form.save()
            return redirect('accueil')
        
        if membre_form.is_valid():
            membre_form.save()
            return redirect('accueil')
    else:
        livre_form = CreationLivreForm()
        dvd_form = CreationDvdForm()
        cd_form = CreationCdForm()
        membre_form = CreationMembreForm()

    livres = Livre.objects.all()
    dvds = Dvd.objects.all()
    cds = Cd.objects.all()
    membres = Membre.objects.all()
    medias = Media.objects.all()

    return render(request, 'accueil.html',{
        'CreationLivre': livre_form,
        'CreationDvd': dvd_form,
        'CreationCd': cd_form,
        'Livres': livres,
        'Dvds': dvds,
        'Cds': cds,
        'CreationMembre': membre_form,
        'Membres': membres,
        'Medias': medias,
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

    return render(request, 'modifier_dvd.html', {'form': form, 'dvd': dvd})

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

    return render(request, 'modifier_cd.html', {'form': form, 'cd': cd})

# Supprimer un CD
@login_required
def supprimer_cd(request, cd_id):
    cd = get_object_or_404(Cd, id=cd_id)
    if request.method == 'POST':  # Confirmation avant suppression
        cd.delete()
        return redirect('accueil')

    return render(request, 'supprimer_dvd.html', {'cd': cd})

# Modifier un Membre
@login_required
def modifier_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    if request.method == 'POST':
        form = CreationMembreForm(request.POST, instance=membre)
        if form.is_valid():
            form.save()
            return redirect('accueil')
    else:
        form = CreationMembreForm(instance=membre)

    return render(request, 'modifier_membre.html', {'form': form, 'membre': membre})

# Supprimer un Membre
@login_required
def supprimer_membre(request, membre_id):
    membre = get_object_or_404(Membre, id=membre_id)
    if request.method == 'POST':  # Confirmation avant suppression
        membre.delete()
        return redirect('accueil')

    return render(request, 'supprimer_membre.html', {'membre': membre})

#Litse de Medias publique
def liste_livres_publique(request):
    Livres = Livre.objects.all()
    return render(request, 'liste_livres_publique.html',{'Livres':Livres})

def liste_cds_publique(request):
    Cds = Cd.objects.all()
    return render(request,'liste_cds_publique.html',{'Cds':Cds})

def liste_dvds_publique(request):
    Dvds = Dvd.objects.all()
    return render(request,'liste_dvds_publique.html',{'Dvds':Dvds})

@login_required
def emprunter(request, media_id,membre_id):
    media = get_object_or_404(Media, id=media_id)
    membre = get_object_or_404(Membre, id=membre_id)

    # Vérifier si le média est disponible
    if not media.disponible:
        messages.error(request, "Ce média est déjà emprunté.")
        return redirect('accueil')
    
    # Vérifier si le membre a déjà 3 emprunts en cours
    emprunts_actifs = Emprunt.objects.filter(membre=membre).count()
    if emprunts_actifs >= 3:
        messages.error(request, "Vous avez atteint la limite de 3 emprunts simultanés.")
        return redirect('accueil')

    # Créer l'emprunt
    Emprunt.objects.create(
        media=media,
        membre=membre,
        date_emprunt=timezone.now(),
        date_retour_prevu = timezone.now() + timedelta(days=7)  # Retour dans 7 jours
    )

    # Marquer le média comme indisponible
    media.disponible = False
    media.save()

    messages.success(request, f"Vous avez emprunté '{media.nom}' avec succès jusqu'au {Emprunt.date_retour_prevu}.")
    return redirect('accueil')

@login_required
def restituer(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    # Vérifier si un emprunt existe pour ce média et ce membre
    emprunt = Emprunt.objects.get(media=media, date_retour__isnull=True)

    if not emprunt:
        messages.error(request, "Média non emprunté")
        return redirect('accueil')
    
    # Mettre à jour l'état du média
    media.disponible = True
    media.save()

    # Marquer l'emprunt comme terminé
    emprunt.date_retour = timezone.now()
    emprunt.save()

    messages.success(request, f"Le média {media.nom} a été restitué avec succès.")
    return redirect('accueil')