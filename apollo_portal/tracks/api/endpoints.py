"""Web API for async requests from client."""

from django.http import JsonResponse
from django.db.models.functions import Lower

from apollo_portal.utils.api import api_view
from tracks.models import Genome


@api_view(['GET'])
def genomes(request):
    """Return requested genomes as json."""
    genomes = Genome.objects.all()
    filter_labs = request.GET.get('labs')
    if filter_labs:
        labs = filter_labs.split(',')
        genomes = (
            genomes
            .annotate(lab_lower_name=Lower('lab__name'))
            .filter(lab_lower_name__in=labs)
        )
    return JsonResponse({'genomes': [
        g.as_json()
        for g in genomes
    ]})
