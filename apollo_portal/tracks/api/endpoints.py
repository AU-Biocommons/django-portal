"""Web API for async requests from client."""

from django.http import JsonResponse
from django.db.models.functions import Lower

from apollo_portal.utils.api import api_view
from tracks.models import Genome, Lab, Track


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
    filter_group = request.GET.get('group')
    if filter_group:
        # Case insensitive filter by genome.group.name
        genomes = genomes.filter(group__name__iexact=filter_group)
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


@api_view(['GET'])
def tracks(request):
    """Return requested genomes as json."""
    tracks = Track.objects.all()
    filter_keywords = {
        'group': 'genome__group__name__iexact',
        'genome_id': 'genome__id',
    }
    filter_kwargs = {
        kwarg: request.GET.get(param)
        for param, kwarg in filter_keywords.items()
        if request.GET.get(param)
    }
    tracks = tracks.filter(**filter_kwargs)
    return JsonResponse({'tracks': [
        t.as_json()
        for t in tracks
    ]})
