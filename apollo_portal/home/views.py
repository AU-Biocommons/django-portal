from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def signup(request):
    # TODO
    return render(request, 'home/signup.html')


def contact(request):
    # TODO
    return render(request, 'home/contact.html')


def getting_started(request):
    return render(request, 'home/resources/getting-started.html')


def documentation(request):
    return render(request, 'home/resources/documentation.html')


def training(request):
    # TODO
    return render(request, 'home/resources/training.html')


def faqs(request):
    # TODO
    return render(request, 'home/resources/faqs.html')


def video(request):
    # TODO
    return render(request, 'home/resources/video.html')


def terms(request):
    return render(request, 'home/resources/terms.html')
