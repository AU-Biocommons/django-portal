from django.contrib import admin

from .models import Genome, Lab, Track

admin.site.register(Genome)
admin.site.register(Lab)
admin.site.register(Track)
