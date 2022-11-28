from django.db import models
from django.urls import reverse
# Create your models here\
from django.core.validators import MinValueValidator, MaxValueValidator




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
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]

    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)



    def __str__(self):
        if self.gender == self.MALE:

            return f"Актер {self.first_name}  {self.last_name}"
        elif self.gender == self.FEMALE:
            return f"Актриса {self.first_name} {self.last_name}"

    def get_url(self):
        return reverse('one_actors', args=[self.id])



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
    budget = models.IntegerField(default=1000000, blank=True, validators=[MinValueValidator(1)])

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=RUB)
    slug = models.SlugField(default='', null=False, db_index=True)
    director = models.ForeignKey(Directors, on_delete=models.CASCADE, null=True)
    actors = models.ManyToManyField(Actors)

    def __str__(self):
        return f"{self.name} {self.rating}%"

    def get_url(self):
        return reverse('one_movie', args=[self.id])