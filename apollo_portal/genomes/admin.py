from django.contrib import admin
from django.utils.html import format_html

from .models import Genome, Lab, Track


class GenomeAdmin(admin.ModelAdmin):
    list_display = [
        "name", "group", "_lab_name", "species", "strain", "datetime_created"]

    @admin.display(ordering="genome__name")
    def _genome_name(self, track):
        return track.genome.name

    @admin.display(ordering="lab__name")
    def _lab_name(self, genome):
        return format_html(
            '<a href="/admin/genomes/lab/{}/">{}</a>',
            genome.lab.id,
            genome.lab.name,
        )


class TrackAdmin(admin.ModelAdmin):
    list_display = ["name", "_genome_name", "_lab_name", "datetime_created"]

    @admin.display(ordering="genome__name")
    def _genome_name(self, track):
        return format_html(
            '<a href="/admin/genomes/genome/{}/">{}</a>',
            track.genome.id,
            track.genome.name,
        )

    @admin.display(ordering="lab__name")
    def _lab_name(self, track):
        return format_html(
            '<a href="/admin/genomes/lab/{}/">{}</a>',
            track.lab.id,
            track.lab.name,
        )


admin.site.register(Lab)
admin.site.register(Genome, GenomeAdmin)
admin.site.register(Track, TrackAdmin)
