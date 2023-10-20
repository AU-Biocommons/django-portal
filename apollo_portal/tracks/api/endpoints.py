"""Web API for async requests from client."""

from django.http import JsonResponse
from django.db.models.functions import Lower

from apollo_portal.utils.api import api_view
from tracks.models import Genome, Lab


@api_view(['GET'])
def labs(request):
    """Return requested labs as json."""
    labs = Lab.objects.all()
    filter_labs_str = request.GET.get('labs')
    if filter_labs_str:
        filter_labs = [
            lab.lower()
            for lab in filter_labs_str.split(',')
        ]
        # Case insensitive filter by lab.name
        labs = (
            labs
            .annotate(lower_name=Lower('name'))
            .filter(lower_name__in=filter_labs)
        )

    return JsonResponse({
        'labs': {
            lab.name: lab.as_json()
            for lab in labs
        }
    })


@api_view(['GET'])
def genomes(request):
    """Return requested genomes as json."""
    genomes = Genome.objects.all()
    filter_labs_str = request.GET.get('labs')
    if filter_labs_str:
        labs = [
            lab.lower()
            for lab in filter_labs_str.split(',')
        ]
        # Case insensitive filter by genome.lab.name
        genomes = (
            genomes
            .annotate(lab_lower_name=Lower('lab__name'))
            .filter(lab_lower_name__in=labs)
        )

    return JsonResponse({'genomes': [
        g.as_json()
        for g in genomes
    ]})
