"""Web API for async requests from client."""

from django.http import JsonResponse

from apollo_portal.utils.api import api_view
from tracks.models import Genome


@api_view(['GET'])
def genomes(request):
    """Return requested genomes as json.

    TODO: filter on query params (so we can hit this endpoint to get genomes
          for e.g. a specific lab)

    """
    return JsonResponse({'genomes': [
        g.as_json()
        for g in Genome.objects.all()
    ]})
