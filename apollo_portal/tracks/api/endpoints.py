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
        labs = [
            lab.lower()
            for lab in filter_labs.split(',')
        ]
        # Case insensitive filter by genome.lab.name
        genomes = (
            genomes
            .annotate(lab_lower_name=Lower('lab__name'))
            .filter(lab_lower_name__in=labs)
        )

    data = {'genomes': [
        g.as_json()
        for g in genomes
    ]}

    return JsonResponse(data)
