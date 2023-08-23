"""Views for degnan group."""

from django.shortcuts import render


def index(request):
    return render(request, 'home/groups/degnan/index.html')


def cots(request):
    return render(request, 'home/groups/degnan/cots.html')


def amphimedon(request):
    return render(request, 'home/groups/degnan/amphimedon.html')
