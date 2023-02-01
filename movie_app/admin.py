from django.contrib import admin
from .models import Directors, Actors, Movie, Genres, Cinema, Showtime, Seat


# Register your models here.

admin.site.register(Directors)
admin.site.register(Actors)
admin.site.register(Genres)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'budget']
    list_editable = ['rating', 'budget']
    ordering = ['-rating', '-name']
    list_per_page = 10
    actions = ['set_dollars', 'set_euro']
    filter_horizontal = ['actors', 'genres', 'cinemas']


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['show_movies']




@admin.register(Showtime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'cinema', 'movie')
    search_fields = ('cinema__name', 'movie__name')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_available', 'showing')
    search_fields = ('name', 'showing__cinema__name', 'showing__movie__name')

