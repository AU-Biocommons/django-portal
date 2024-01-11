"""Views for degnan group."""

from django.shortcuts import render
from django.views import View

from .forms import ContactForm


class ContactView(View):
    """Tradis contact-us view."""

    def get(self, request):
        """Get request."""
        form = ContactForm()
        return render(request, 'home/groups/tradis/contact.html', {
            'form': form,
        })

    def post(self, request):
        """Post request."""
        form = ContactForm(request.POST)
        if form.is_valid():
            form.dispatch()
            return render(request, 'home/groups/tradis/contact-success.html')
        return render(request, 'home/groups/tradis/contact.html', {
            'form': form,
        })


def index(request):
    return render(request, 'home/groups/tradis/index.html')


def tutorial(request):
    return render(request, 'home/groups/tradis/tutorial.html')
