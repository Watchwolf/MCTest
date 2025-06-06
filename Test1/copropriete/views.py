from django.shortcuts import render, redirect
from .models import Copropriete


def stats(request):
    """
    Vue pour afficher les statistiques selon le filtre fournit par l'utilisateur (ville, code postal, département)
    """
    filter: str = None

    stats = None
    if request.method == 'GET':
        filter = request.GET.get('filter', '').strip()
        if filter:
            stats = Copropriete.stats(filter)

    context = {
        'filter': filter if filter else '',
        'stats': stats,
    }
    return render(request, 'templates/copropriete/stats.html', context)

def add(request):
    """
    Vue pour ajouter une copropriete à partir de son URL
    """
    if request.method == 'POST':
        Copropriete.add_to_dataset(request.POST.get('url', None))
        return redirect('/copropriete/stats')

    
    return render(request, 'templates/copropriete/add.html', {})