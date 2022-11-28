from django.shortcuts import render
from .models import Directors,  Actors, Movie
from django.db.models import F, Sum, Max, Min, Count, Avg
from django.shortcuts import get_object_or_404

def show_all_movies(request):
    movies = Movie.objects.all()
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    return render(request, 'movie/all_movies.html', {
        'movies': movies,
        'agg': agg,
        'total': movies.count()
    })

def one_movie(request, id_mov: int):
    movie = get_object_or_404(Movie, id=id_mov)
    return render(request, 'movie/one_movie.html', {
        'mov': movie
    })

def index(request):
    return render(request, 'movie/base.html')


def all_directors(request):
    directors = Directors.objects.all()
    return render(request, 'movie/all_directors.html', {
        'directors':directors
    })

def one_director(request, id_dir: int):
    dir = get_object_or_404(Directors, id=id_dir)
    return render(request, 'movie/one_dir.html', {
        'dir': dir
    })


def all_actors(request):
    actors = Actors.objects.all()
    return render(request, 'movie/all_actors.html', {
        'actors': actors
    })

def one_actor(request, id_act: int):
    act = get_object_or_404(Actors, id=id_act)
    return render(request, 'movie/one_actors.html', {
        'act': act
    })


