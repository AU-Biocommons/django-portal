from django.shortcuts import render


def organisms(request):
    return render(request, 'tracks/organisms.html')
