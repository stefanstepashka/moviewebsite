from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import Directors,  Actors, Movie, Genres, UserFavourites, Cinema, Seat, Showtime, Reservation
from .forms import ReservationForm
from django.db.models import F, Sum, Max, Min, Count, Avg
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse
from django.db import connection
print(connection.queries)

def show_all_movies(request):
    sort = request.GET.get('sort')
    query = request.GET.get('q')
    genre = request.GET.get('genre')
    movies = Movie.objects.all()

    if query:
        movies = Movie.objects.filter(name__icontains=query)

    if genre:
        movies = movies.filter(genres__genre__exact=genre)
        genres = Genres.objects.filter(genre=genre)
    else:
        genres = Genres.objects.filter(movie__in=movies).distinct()

    if sort:
        if sort == 'high':
            movies = movies.order_by('-rating')
        elif sort == 'low':
            movies = movies.order_by('rating')
    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Count('id'))
    paginator = Paginator(movies, 5)
    page = request.GET.get('page')
    movies = paginator.get_page(page)
    movie_count = agg['id__count']

    return render(request, 'movie/all_movies.html', {
        'movies': movies,
        'agg': agg,
        'total': movie_count,
        'genres': genres

    })


def one_movie(request, id_mov: int):
    movie = get_object_or_404(
        Movie.objects.all().prefetch_related('cinemas'), id=id_mov)

    cinemas = movie.cinemas.select_related('showtime').values('id',
    'name')

    return render(request, 'movie/one_movie.html', {
        'mov': movie,
        'cinemas': cinemas


    })


def cinema_detail(request, cinema_id):
    cinema = get_object_or_404(Cinema.objects.prefetch_related(
        'show_movies').only('pk', 'show_movies__name',
        'location', 'capacity', 'name'), id=cinema_id)
    movies = cinema
    showtimes = Showtime.objects.filter(cinema=cinema)
    return render(request, 'movie/cinema_detail.html', {
        'cinema': cinema, 'movies': movies,
        'showtimes': showtimes})


def reserve_seat(request, cinema_id, seat_id):
    seat = Seat.objects.get(id=seat_id)
    cinema = Cinema.objects.get(id=cinema_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.seat = seat
            reservation.save()
            seat.is_available = False
            seat.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'movie/reserve_seat.html', {'form': form, 'seat': seat})


def confirmation(request):
    return HttpResponse("Reservation Confirmed!")


def index(request):
    return render(request, 'movie/base.html')


def all_directors(request):
    directors = Directors.objects.all().only('first_name', 'last_name')
    search_query = request.GET.get('q')
    if search_query:
        directors = Directors.objects.filter(Q(
            first_name__icontains=search_query) | Q(
            last_name__icontains=search_query)).only('first_name',
                                                       'last_name')

    paginator = Paginator(directors, 10)
    page = request.GET.get('page')
    directors = paginator.get_page(page)
    return render(request, 'movie/all_directors.html', {
        'directors':directors,
        'search_query': search_query
    })


def one_director(request, id_dir: int):
    dir = get_object_or_404(Directors.objects.all().values('first_name',
                                                           'last_name',
                                                           'email'), id=id_dir)
    return render(request, 'movie/one_dir.html', {
        'dir': dir
    })


def all_actors(request):
    actors = Actors.objects.all()
    search_query = request.GET.get('q')
    paginator = Paginator(actors, 10)
    page = request.GET.get('page')
    actors = paginator.get_page(page)
    if search_query:
        actors = Actors.objects.filter(first_name__icontains=search_query)
    return render(request, 'movie/all_actors.html', {
        'actors': actors,
        'search_query': search_query
    })


def one_actor(request, id_act: int):
    act = get_object_or_404(Actors, id=id_act)
    return render(request, 'movie/one_actors.html', {
        'act': act
    })


@login_required
def personal_cabinet(request):
    user = request.user

    favorites = UserFavourites.objects.filter(user=user)

    if request.method == 'POST':
        favorite_id = request.POST.get('favorite_id')
        favorite = get_object_or_404(UserFavourites, id=favorite_id, user=user)
        favorite.delete()
    return render(request, 'movie/personal_cabinet.html', {'favorites': favorites})


@login_required
def my_reservations(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).select_related('seat__showing__movie', 'seat__showing__cinema')

    print(reservations)
    return render(request, 'personal_cabinet/my_reservation.html', {'reservations': reservations})


@login_required
def cancel_reservation(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    seat = reservation.seat
    seat.is_available = True
    seat.save()
    reservation.delete()
    return redirect('my_reservations')


@login_required
def add_to_personal(request):
    if request.method == 'POST':
        user = request.user
        movie_id = request.POST.get('movie')
        movie = get_object_or_404(Movie, id=movie_id)
        if UserFavourites.objects.filter(user=user, movie=movie).exists():
            messages.error(request, 'This movie has already been added to your favorites')
        else:
            UserFavourites.objects.create(user=user, movie=movie)
            messages.success(request, 'Movie added to favorites')
        return redirect('movies')


@login_required
def favorites(request):
    user = request.user
    favorites = UserFavourites.objects.filter(user=user)
    return render(request, 'movie/favorites.html', {'favorites': favorites})


#login
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'movie/signup.html'


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'movie/login.html'
    success_url = '/movie/base/'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect('movies')
        else:
            return self.form_invalid(form)


class LogoutView(generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)



