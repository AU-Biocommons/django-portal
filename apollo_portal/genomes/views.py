"""Tracks views."""

from django.shortcuts import get_object_or_404, render

from genomes.models import Genome


def genomes(request):
    """Genomes list/filter view."""
    return render(request, 'genomes/genomes.html')


def tracks(request, genome_id):
    """Tracks table view."""
    genome = get_object_or_404(Genome, id=genome_id)
    return render(request, 'genomes/tracks.html', {
        'genome': genome.as_json(),
    })
