from django.db import models
from django.urls import reverse
# Create your models here\
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

#Genre of the movie


class Genres(models.Model):
    comedy = 'comedy'
    drama = 'drama'
    western = 'western'
    science = 'science fiction'
    fantasy = 'fantasy'
    horror = 'horror'
    psycho_thriller = 'psychological thriller'
    romance = 'romance'
    GENRES = [
        (comedy, 'Comedy'),
        (drama, 'Drama'),
        (western, 'Western'),
        (science, 'Science Fiction'),
        (fantasy, 'Fantasy'),
        (horror, 'Horror'),
        (psycho_thriller, 'Psychological Thriller'),
        (romance, 'Romance')
    ]

    genre = models.CharField(max_length=22, choices=GENRES)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['genre'], name='unique_genre')
        ]
    def __str__(self):
        return f"{self.genre}"
#DIRECTORS


class Directors(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default='@mail.ru')

    def get_url(self):
        return reverse('one_director', args=[self.id])

    def __str__(self):
        return f"{self.first_name }  {self.last_name}"


#ACTORS
class Actors(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    MALE = 'Male'
    FEMALE = 'Female'

    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]

    gender = models.CharField(max_length=6, choices=GENDERS, default=MALE)

    def __str__(self):
        if self.gender == self.MALE:

            return f"Актер {self.first_name}  {self.last_name}"
        elif self.gender == self.FEMALE:
            return f"Актриса {self.first_name} {self.last_name}"

    def get_url(self):
        return reverse('one_actors', args=[self.id])


#Main model

class UserFavourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='favorites')
    date_added = models.DateTimeField(auto_now_add=True)






class Movie(models.Model):
    EUR = 'EUR'
    DOL = 'DOL'
    RUB = 'RUB'
    CURRENCY_CHOICES = [
        (EUR, 'Euro'),
        (DOL, 'Dollar'),
        (RUB, 'Rubles')
    ]
    name = models.CharField(max_length=40)
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                 MaxValueValidator(100)])
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(
        default=1000000, blank=True,
        validators=[MinValueValidator(1)])

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES, default=RUB)
    slug = models.SlugField(default='', null=False, db_index=True)
    director = models.ManyToManyField(Directors)
    actors = models.ManyToManyField(Actors)
    genres = models.ManyToManyField(Genres)
    cinemas = models.ManyToManyField(
        'Cinema', related_name='cinema')

    def __str__(self):
        return f"{self.name} {self.rating}%"

    def get_url(self):
        return reverse('one_movie', args=[self.id])

    def get_absolute_url(self):
        return reverse('one_movie', args=[str(self.id)])

class Cinema(models.Model):
    name = models.CharField(
        max_length=100)
    location = models.CharField(
        max_length=200)
    capacity = models.IntegerField(
        default=1)
    show_movies = models.ManyToManyField(Movie)


    def create_seats(self):
        seats = [Seat(name=f'{row}{col}', showing=Showtime) for row in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for col in
                 range(1, 11)]
        Seat.objects.bulk_create(seats)
    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('one_movie', args=[str(self.id)])

class Showtime(models.Model):
    start_time = models.DateTimeField()
    cinema = models.ForeignKey(
        Cinema,
        on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE)

    def __str__(self):
        return f"Кинотеатр {self.cinema} фильм {self.movie}"

class Seat(models.Model):
    name = models.CharField(
        max_length=10, null=True)
    is_available = models.BooleanField(
        default=True)
    showing = models.ForeignKey(
        Showtime, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE)
    customer_name = models.CharField(
        max_length=100)
    customer_email = models.EmailField()
    showing_at = models.ForeignKey(
        Showtime, on_delete=models.CASCADE,
        null=True)

    reservation_date = models.DateTimeField(
        auto_now_add=True)