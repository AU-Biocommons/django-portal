from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def terms(request):
    return render(request, 'home/resources/terms.html')


def getting_started(request):
    return render(request, 'home/resources/getting-started.html')
