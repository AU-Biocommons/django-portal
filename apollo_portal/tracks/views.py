from django.shortcuts import render


def genomes(request):
    """Genomes list/filter view.

    Genomes are fetched from the API.
    """
    return render(request, 'tracks/genomes.html')
