from django.urls import path, include
from .redirects import redirect_patterns
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_pages, name='search'),
    path('about/', views.about, name='about'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('resources/', views.resources, name='resources'),
    path('resources/start/',
         views.getting_started,
         name='getting_started'),
    path('resources/documentation/',
         views.documentation,
         name='documentation'),
    path('resources/training/', views.training, name='training'),
    path('resources/faqs/', views.faqs, name='faqs'),
    path('resources/video/', views.video, name='video'),
    path('resources/terms/', views.terms, name='terms'),
    path('notice/<int:notice_id>', views.notice, name='notice'),
    path('degnan/', include('home.groups.degnan.urls')),
    path('tradis/', include('home.groups.tradis.urls')),
] + redirect_patterns
