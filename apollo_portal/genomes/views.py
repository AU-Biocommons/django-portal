"""Tracks views."""

from django.shortcuts import render
from genomes.models import Genome


def genomes(request):
    """Genomes list/filter view."""
    return render(request, 'genomes/genomes.html')


def tracks(request, genome_id):
    """Tracks table view."""
    genome = Genome.objects.get(id=genome_id)
    return render(request, 'genomes/genomes.html', {
        'genome': genome.as_json(),
    })
