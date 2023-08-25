import logging
import pprint
from django.shortcuts import render
from django.views import View
from .forms import SignUpForm
from . import search

logger = logging.getLogger('django')


RESOURCES_PAGES = [
    {
        'url': '/resources/start',
        'label': 'Getting Started',
    },
    {
        'url': '/resources/documentation',
        'label': 'User Documentation',
    },
    {
        'url': '/resources/training',
        'label': 'Training, Tutorials and Other Resources',
    },
    {
        'url': '/resources/faqs',
        'label': 'FAQs',
    },
    {
        'url': '/resources/video',
        'label': 'Video Resources',
    },
    {
        'url': '/resources/terms',
        'label': 'Terms of Use',
    },
]


def get_resource_nav_context(request):
    """Return a context dict for prev and next pages."""
    for i, item in enumerate(RESOURCES_PAGES):
        if item['url'] == request.path:
            break
    return {
        'prev': RESOURCES_PAGES[i-1] if i > 0 else None,
        'next': (
            RESOURCES_PAGES[i+1]
            if i < len(RESOURCES_PAGES) - 1
            else None
        ),
    }


class SignupView(View):
    """Allow users to apply for an Apollo service instance."""

    def get(self, request):
        form = SignUpForm()
        return render(request, 'home/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.dispatch()
            return render(request, 'home/signup-success.html')
        else:
            logger.info(
                "Invalid form submission:\n" + pprint.pformat(form.errors))
        return render(request, 'home/signup.html', {'form': form})


class SearchView(View):
    """Search Apollo webpages."""

    def get(self, request):
        query = request.GET.get('q', '')
        if not query:
            return render(request, 'home/search.html', {'query': query})
        else:
            return render(request, 'home/search.html', {
                'query': query,
                'results': search.search(query),
            })


def index(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')


def getting_started(request):
    return render(request, 'home/resources/getting-started.html', {
        'nav': get_resource_nav_context(request),
    })


def documentation(request):
    return render(request, 'home/resources/documentation.html', {
        'nav': get_resource_nav_context(request),
    })


def training(request):
    return render(request, 'home/resources/training.html', {
        'nav': get_resource_nav_context(request),
    })


def faqs(request):
    return render(request, 'home/resources/faqs.html', {
        'nav': get_resource_nav_context(request),
    })


def video(request):
    return render(request, 'home/resources/video.html', {
        'nav': get_resource_nav_context(request),
    })


def terms(request):
    return render(request, 'home/resources/terms.html', {
        'nav': get_resource_nav_context(request),
    })
