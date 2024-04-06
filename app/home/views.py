import logging
import pprint
from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import ContactForm, SignUpForm
from .models import Notice
from . import search

logger = logging.getLogger('django')


RESOURCES_PAGES = [
    {
        'url': '/resources/start/',
        'label': 'Getting Started',
    },
    {
        'url': '/resources/documentation/',
        'label': 'User Documentation',
    },
    {
        'url': '/resources/training/',
        'label': 'Training, Tutorials and Other Resources',
    },
    {
        'url': '/resources/faqs/',
        'label': 'FAQs',
    },
    {
        'url': '/resources/video/',
        'label': 'Video Resources',
    },
    {
        'url': '/resources/terms/',
        'label': 'Terms of Use',
    },
]


def get_resource_nav_context(request):
    """Return a context dict for prev and next pages."""
    for i, item in enumerate(RESOURCES_PAGES):
        if item['url'] == request.path:
            break
    return {
        'prev': RESOURCES_PAGES[i - 1] if i > 0 else None,
        'next': (
            RESOURCES_PAGES[i + 1]
            if i < len(RESOURCES_PAGES) - 1
            else None
        ),
    }


class AbstractFormView(View):
    """Manage generic form submission."""

    Form = None
    Form = SignUpForm
    template = None
    template = 'home/signup.html'
    success_template = None
    success_template = 'home/signup-success.html'

    def get(self, request):
        form = self.Form()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.Form(request.POST)
        if form.is_valid():
            if hasattr(form, 'dispatch'):
                form.dispatch()
            return render(request, self.success_template)
        else:
            logger.info(
                "Invalid form submission:\n" + pprint.pformat(form.errors))
        return render(request, self.template, {'form': form})


class SignupView(AbstractFormView):
    """Handle sign-up form submission."""

    Form = SignUpForm
    template = 'home/signup.html'
    success_template = 'home/signup-success.html'


class ContactView(AbstractFormView):
    """Handle contact form submission."""

    Form = ContactForm
    template = 'home/contact.html'
    success_template = 'home/contact-success.html'


def search_pages(request):
    """Search Apollo webpages."""
    query = request.GET.get('q', '')
    return render(request, 'home/search.html', {
        'query': query,
        'hits': search.search(query),
    })


def index(request):
    """Show landing page with current notices."""
    notices = Notice.objects.filter(enabled=True)
    if not request.user.is_staff:
        notices = notices.filter(is_published=True)
    return render(request, 'home/index.html', {
        'notices': notices,
    })


def notice(request, notice_id):
    """Show notice page."""
    return render(request, 'home/notice.html', {
        'notice': get_object_or_404(Notice, id=notice_id),
    })


def about(request):
    return render(request, 'home/about.html')


def resources(request):
    return render(request, 'home/resources/index.html')


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
