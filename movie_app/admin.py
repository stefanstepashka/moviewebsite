from django.contrib import admin
from .models import Directors, Actors, Movie

# Register your models here.

admin.site.register(Directors)
admin.site.register(Actors)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'director', 'budget']
    list_editable = ['rating', 'director', 'budget']
    ordering = ['-rating', '-name']
    list_per_page = 10
    actions = ['set_dollars', 'set_euro']
    filter_horizontal = ['actors']