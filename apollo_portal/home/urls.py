from django.urls import path
from .redirects import redirect_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('signup', views.signup, name='signup'),
    path('contact', views.contact, name='contact'),
    path('resources/start',
         views.getting_started,
         name='getting_started'),
    path('resources/documentation', views.documentation, name='documentation'),
    path('resources/training', views.training, name='training'),
    path('resources/faqs', views.faqs, name='faqs'),
    path('resources/video', views.video, name='video'),
    path('resources/terms', views.terms, name='terms'),
] + redirect_patterns
